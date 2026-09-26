# AGENTS.md

<!-- 复制到 Flutter 项目根目录。保持短：这份文件每次都会进上下文，每一行都在花 token。 -->
<!-- 只写 agent 从代码里看不出来、或者经常做错的事。 -->

## 环境

- Flutter x.y.z / Dart x.y.z（以 `flutter --version` 为准，不要使用更新版本才有的 API）
- 最低支持：iOS xx / Android minSdk xx
- 状态管理：<!-- 例如 Riverpod 2 / Bloc 8，只用这一种 -->
- 路由：<!-- 例如 go_router -->

## 目录约定

- `lib/features/<feature>/` 下分 `data/`、`domain/`、`presentation/`
- 共享组件放 `lib/shared/widgets/`，新增前先搜索有没有现成的

## 不要做

- 不要编辑生成文件：`*.g.dart`、`*.freezed.dart`、`*.gr.dart`。改了源文件后运行
  `dart run build_runner build --delete-conflicting-outputs`
- 不要改 `ios/Runner.xcodeproj` 的签名配置、`android/app/build.gradle` 的签名和 flavor，需要时先问
- 不要新增 pub 依赖，需要时先说明理由
- 不要使用 `print`，用项目的 logger

## 跨端改动

- platform channel 名称定义在 <!-- 路径 -->
- 改 Dart 侧接口时，同时列出并修改 Android（Kotlin）和 iOS（Swift）对应实现

## 每次改完必须运行

```bash
flutter analyze
flutter test <相关测试文件>
```

失败就修到通过再报告完成。UI 改动附上说明，我会给截图确认。
