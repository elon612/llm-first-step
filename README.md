# llm-first-step

给**每天用 agent 写代码**、但想知道“为什么这么用更好”的开发者。
例子以 Android / iOS / Flutter 应用层开发为主。

一条主线：

```text
先选对概念（00）
        ↓
聊天 = next-token（01）→ agent = 循环 + 工具（02）
        ↓
上下文工程（03）→ 验证与评估（04）
        ↓
模型怎么训出来的（05）→ 成本与延迟（06）
        ↓
分支：App 要加 AI 功能（07）    可选：手写 GPT 的原理路线（deep-dive）
```

每一课都用同一句话解释新东西：**模型只做 next-token，一切能力差异都来自训练和上下文。**

[ROADMAP.md](ROADMAP.md) · [PROGRESS.md](PROGRESS.md)

## 今天

```bash
git clone https://github.com/elon612/llm-first-step.git
cd llm-first-step
python3 src/chat_as_completion.py
python3 src/agent_loop.py
```

先读 [lessons/00-concept-map.md](lessons/00-concept-map.md)，再读 [lessons/01-why-next-token-can-chat.md](lessons/01-why-next-token-can-chat.md)。

## 目录

| 目录 | 放什么 |
| --- | --- |
| [lessons/](lessons/) | 主线课程 00–07 |
| [exercises/](exercises/) | 练习；你写的代码和答案要提交 |
| [templates/](templates/) | 直接复制到你项目里用：`AGENTS.md`（Flutter）、评估任务集、fail-first 门禁脚本 |
| [case-studies/](case-studies/) | 生产问题的完整设计，把课程概念用在真实项目上 |
| [src/](src/) | 离线可跑的演示脚本，不需要 API key |
| [deep-dive/](deep-dive/) | 可选：跟 Karpathy 手写 GPT → LLMs-from-scratch → 推理与微调工程 |

测试：`python3 -m unittest discover -s tests`

硬件：主线只需要能跑 Python 3.10+。练习 02 需要一个模型 API key。只有 deep-dive 的 LoRA 实操需要 GPU。

## 外部资源，主线只留这几个

1. Karpathy — [Deep Dive into LLMs like ChatGPT](https://www.youtube.com/watch?v=7xTGNNLPyMI)（01、05）
2. Anthropic — [Building effective agents](https://www.anthropic.com/research/building-effective-agents)（02）
3. Anthropic — [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)（03）
4. Hamel Husain — [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/)（04）
5. Chip Huyen — *AI Engineering*（07，需要时再读）

## License

MIT. See [LICENSE](LICENSE).
