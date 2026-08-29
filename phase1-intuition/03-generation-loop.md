# 03. 生成循环：同一个目标，训练和推理

训练标签无聊得可以：

```text
Input :  The cat sat on the
Target:  mat
```

窗口一次滑一个 token，扫过整份语料。损失是交叉熵：模型对真正的下一个 token 有多惊讶。

推理时没有人给答案。模型吐出词表上的概率，然后有人挑一个。

## 怎么挑

| 策略 | 行为 |
| --- | --- |
| greedy（argmax） | 永远最高分。稳，容易重复 |
| temperature &lt; 1 | 分布更尖，更保守 |
| temperature = 1 | 原始分布 |
| temperature &gt; 1 | 更平，更意外，也更胡说 |
| top-k / top-p | 丢掉长尾再采样 |

自己感受：

```bash
python3 src/next_token_demo.py
python3 src/next_token_demo.py --prompt "The little cat" --greedy
python3 src/next_token_demo.py --prompt "小猫" --temperature 1.2
```

字符 bigram 只看前一个字符，故事很快崩。这不是 bug，这是在告诉你：**上下文有多长，智能就有多真。**

Transformer 把“前一个字符”换成“整段 prompt”。循环不变。

## 和聊天的关系

`src/chat_as_completion.py` 已经把对话变成字符串。
`src/next_token_demo.py` 让你看见循环本身。

两者合在一起就是托管 API：

```text
messages JSON  →  拼成 token 序列  →  循环采样  →  把新 token 解码成 assistant 文本
```

可选：`src/chat_hello.py` 会打一次真模型。那是验证，不是这一阶段的主线。没有 key 就跳过。

## 这一课结束的标准

能画出：

```text
prompt → score → pick → append → repeat
```

并指出玩具模型和 GPT 的唯一本质差别：每次预测能看见多少上下文、权重有多好。不要在这里开始推导 Q/K/V。
