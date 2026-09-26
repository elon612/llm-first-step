#!/usr/bin/env bash
# fail_first_check.sh — 分支里新增或修改的测试，必须在改动前的代码上失败。
#
# 一条测试在修复前后都通过，就证明不了它能抓住这次的 bug：
# 要么是同义反复，要么测偏了地方。修复前的代码就是一个现成的“变异体”。
#
# 每条测试跑两次：当前代码上必须通过（排除环境故障），改动前的代码上必须失败。
# 重命名按“新增”处理，改名时顺手放宽断言也会被检查到。
#
# 用法：
#   fail_first_check.sh [base-ref]            # 默认 origin/main
#
# 环境变量：
#   TEST_PATH_RE     要回放的测试文件（默认 test/ 下的 *_test.dart；integration_test 需要设备，默认不跑）
#   TEST_SUPPORT_RE  需要一起带到旧代码上的文件，如 fixture、fake（默认 test/、integration_test/ 下所有文件）
#   SRC_PATH_RE      实现文件（默认 lib/ 下的 .dart）；分支没有改实现时直接跳过
#   RUN_TESTS        在仓库根目录执行的命令，最后一个参数是测试文件路径；
#                    默认按最近的 pubspec.yaml 分包运行 flutter test / dart test
#   REQUIRE_TEST=1   改了实现却没有任何测试改动时判失败（默认只告警）
#
# 豁免：分支内任一提交信息含一行 `Fail-First: skip <理由>`（纯重构、性能优化等不改行为的改动）。
#
# 退出码：0 通过或跳过；1 有测试在改动前就通过，或 REQUIRE_TEST=1 时缺测试；
#         2 用法错误，或测试在当前代码上就失败（环境问题或测试本身是坏的，无法判断）。

set -euo pipefail

base_ref="${1:-origin/main}"
TEST_PATH_RE="${TEST_PATH_RE:-(^|/)test/.*_test\.dart$}"
TEST_SUPPORT_RE="${TEST_SUPPORT_RE:-(^|/)(test|integration_test)/}"
SRC_PATH_RE="${SRC_PATH_RE:-(^|/)lib/.*\.dart$}"

root="$(git rev-parse --show-toplevel)"
cd "$root"

if ! base="$(git merge-base "$base_ref" HEAD 2>/dev/null)"; then
  echo "fail-first: 找不到 base ref: $base_ref" >&2
  exit 2
fi

if git log --format=%B "$base..HEAD" | grep -qiE '^Fail-First: skip'; then
  echo "fail-first: 提交信息声明了豁免，跳过"
  git log --format=%B "$base..HEAD" | grep -iE '^Fail-First: skip' | sed 's/^/  /'
  exit 0
fi

changed="$(git diff --name-only --no-renames --diff-filter=AM "$base" HEAD)"
tests="$(grep -E "$TEST_PATH_RE" <<<"$changed" || true)"
support="$(grep -E "$TEST_SUPPORT_RE" <<<"$changed" || true)"
src="$(grep -E "$SRC_PATH_RE" <<<"$changed" || true)"

if [[ -z "$src" ]]; then
  echo "fail-first: 没有实现改动，跳过（为存量代码补的测试本来就应该在旧代码上通过）"
  exit 0
fi

if [[ -z "$tests" ]]; then
  echo "fail-first: 改了实现，但没有新增或修改任何测试"
  if [[ "${REQUIRE_TEST:-0}" == "1" ]]; then
    exit 1
  fi
  exit 0
fi

wt="$(mktemp -d)"
cleanup() {
  git worktree remove --force "$wt" >/dev/null 2>&1 || true
  rm -rf "$wt"
}
trap cleanup EXIT
git worktree add --detach --quiet "$wt" "$base"

while IFS= read -r f; do
  [[ -z "$f" ]] && continue
  mkdir -p "$wt/$(dirname "$f")"
  git show "HEAD:$f" >"$wt/$f"
done <<<"$support"

run_default() {
  local file="$1" dir
  dir="$(dirname "$file")"
  while [[ "$dir" != "." && ! -f "$dir/pubspec.yaml" ]]; do
    dir="$(dirname "$dir")"
  done
  if [[ ! -f "$dir/pubspec.yaml" ]]; then
    echo "fail-first: $file 找不到所属的 pubspec.yaml" >&2
    return 2
  fi
  local rel="${file#"$dir"/}"
  (
    cd "$dir"
    if grep -qE '^[[:space:]]*sdk:[[:space:]]*flutter' pubspec.yaml; then
      flutter pub get >/dev/null && flutter test "$rel"
    else
      dart pub get >/dev/null && dart test "$rel"
    fi
  )
}

run_one() {
  local where="$1" file="$2"
  if [[ -n "${RUN_TESTS:-}" ]]; then
    (cd "$where" && bash -c "$RUN_TESTS \"\$1\"" _ "$file")
  else
    (cd "$where" && run_default "$file")
  fi
}

log="$wt/.fail-first.log"
offenders=()
while IFS= read -r f; do
  [[ -z "$f" ]] && continue
  if ! run_one "$root" "$f" >"$log" 2>&1; then
    echo "fail-first: $f 在当前代码上就失败，无法判断（环境问题，或者测试本身是坏的）：" >&2
    tail -n 20 "$log" | sed 's/^/  /' >&2
    exit 2
  fi
  if run_one "$wt" "$f" >"$log" 2>&1; then
    offenders+=("$f")
  else
    echo "fail-first: ok  $f 在改动前失败"
  fi
done <<<"$tests"

if ((${#offenders[@]})); then
  echo
  echo "fail-first: 以下测试在改动前的代码上就已经通过，证明不了这次改动："
  printf '  %s\n' "${offenders[@]}"
  echo
  echo "先确认它断言的是用户可观察的行为，而不是实现细节；"
  echo "不改行为的重构，在提交信息里写 'Fail-First: skip <理由>'。"
  exit 1
fi

echo "fail-first: 全部通过"
