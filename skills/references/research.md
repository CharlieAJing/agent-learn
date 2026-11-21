# 资料检索

## 检索流程

1. 从提纲或用户提问中明确待查问题，将已有判断作为待验证的假设。
2. 按问题[选择来源](#来源选择)，覆盖不足时围绕缺口自由检索。遇到相关配图，打开原图，对照图注与正文阅读。
3. 按问题比对证据及适用条件，交叉核验关键结论。同一研究的多处转述只算一份证据。有分歧时回查原始出处。适用条件不同，分别说明各自的条件与结论。同一条件下仍有冲突，保留分歧并注明出处。
4. 证据足以回答问题时停止检索。记录结论、适用条件和出处（链接及章节）。补查后仍无可靠依据的，标明缺口及待核实点。

## 检索分工

简单核对由主 Agent 完成。需分头查阅、比对多份材料时，由子 Agent 并行检索，各自回传主 Agent。

- 主 Agent 明确共同问题、分配来源，提供必要背景和规范路径。
- 子 Agent 使用独立上下文（`fork_turns: "none"`）并行查阅，各自将结论及依据、适用条件、出处和分歧或缺口直接回传主 Agent，必要时附短摘录。
- 主 Agent 按问题整合结果，完成核验，指出已有判断中需要修正之处。

## 来源选择

- 学习概念、原理或方法，围绕同一问题并行查阅对应主题下各本教材的相关章节，选用依据可靠、切题易懂的材料。
- 核实产品当前行为，优先查官方文档。
- 核实具体实验结果，优先查原始论文或实验报告。

### 大语言模型与 RAG

- 中国人民大学[《大语言模型》](https://llmbook-zh.github.io/) — 中文术语与整体框架。
- [《Speech and Language Processing》](https://web.stanford.edu/~jurafsky/slp3/index.html) — 检索与生成的原理，见[第 11 章](https://web.stanford.edu/~jurafsky/slp3/11.pdf)。
- [《Hands-On Large Language Models》](https://github.com/HandsOnLLM/Hands-On-Large-Language-Models) — 图解与执行过程，见[第 8 章示例](https://github.com/HandsOnLLM/Hands-On-Large-Language-Models/blob/main/chapter08/Chapter%208%20-%20Semantic%20Search.ipynb)。
- 上海交通大学[《动手学大模型》](https://github.com/Lordog/dive-into-llms) — 中文编程实验。

### 信息检索与评估

- [《Introduction to Information Retrieval》](https://nlp.stanford.edu/IR-book/information-retrieval-book.html) — 倒排索引（第 1 章）、评分与排序（第 6 章）、检索评估（第 8 章）。
- [《Search Engines: Information Retrieval in Practice》](https://ciir.cs.umass.edu/downloads/SEIRiP.pdf) — 搜索系统实现与检索实验设计。
- [《Speech and Language Processing》第 11 章](https://web.stanford.edu/~jurafsky/slp3/11.pdf) — 稠密检索及其在 RAG 中的应用。

### 深度学习

- [《动手学深度学习》](https://zh.d2l.ai/) — 算法、公式与代码实现。
- 邱锡鹏[《神经网络与深度学习》](https://github.com/nndl/nndl) — 中文概念与数学推导。
- Simon Prince [《Understanding Deep Learning》](https://udlbook.github.io/udlbook/) — 模型图解与配套习题。

### 其他主题

优先查对应领域的教材或专业课程。

### 有惊喜的一线资料（前沿研究与工程实践）

- [OpenAI Cookbook](https://developers.openai.com/cookbook)
- [Anthropic 工程博客](https://www.anthropic.com/engineering)
- [Google DeepMind 研究](https://deepmind.google/research/)
- [Hugging Face 模型训练团队](https://huggingface.co/HuggingFaceTB)

### 维基百科

查术语、别名、背景与沿革，沿条目引文核实关键结论。
