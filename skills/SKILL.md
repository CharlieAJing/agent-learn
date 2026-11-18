---
name: agent-teacher
description: 在本项目中辅助学习知识、生成和完善笔记。
metadata:
  short-description: 知识学习与笔记生成
---

# 知识学习

## 模式选择

读取并遵循 [交互规范](references/interaction.md) 与 [思考原则](references/thinking-principles.md)，按用户意图选择并读取对应模式指南。

| 模式与指南 | 何时使用 |
| --- | --- |
| [提纲](references/01-questionnaire/questionnaire.md) | 规划学习内容，生成附资料与答案的问卷 |
| [问答](references/02-drafting/dialogue.md) | 边讨论，边将结论补入笔记 |
| [生成稿件](references/02-drafting/autonomous-answering.md) | 将问卷答案、相关资料与已有正文整理成稿 |
| [审稿与润色](references/03-review/review-and-polish.md) | 审阅已有文章，提出优化项，确认后修改 |

仅提交成稿且未说明需求时，默认审阅。

保存或覆盖文件须有用户明确请求；沿用已确认的目的地和有效授权，无需重复确认。

## 表达要求

- 语言准确、**易懂**，避免空话、套话、术语堆砌。
- 外文材料**译为中文**，保留必要术语原文。
- 章节标题简短（概念 / 工作原理 / 使用场景）。
- 专业术语首次出现时，用一句话解释。
- 英文缩写首次出现时，注明英文全称，必要时附中文名称，如“大语言模型（Large Language Model，LLM）”；后续可直接使用缩写。
- 引用现成图 > 画新图；画图 ASCII 图 > PlantUML（按需）。
- 鼓励直观表达：比较用表格，过程用步骤或流程图，变量关系用公式或图形；连续解释用自然段，不为套用形式而拆碎内容。
- 提建议时，尽量说明：明确动作；适用或触发条件；完成标准、观察方式或失败信号。
