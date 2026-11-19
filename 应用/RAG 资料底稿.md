# RAG 资料底稿

对应 [[应用/RAG|RAG 提纲]]。以下聚焦文档问答，保留论文设定、产品行为与实验推断各自的适用条件。

## 概念与组成 · A01

- **定义与微调**。生成以针对当前输入检索到的外部资料为条件。原论文把模型参数中的知识与可检索的外部记忆结合，也对系统做了微调。因此应从“这次回答如何取得资料”和“模型参数如何学得”两个维度比较。直接返回搜索结果只完成了检索。 [Lewis 等，摘要](https://arxiv.org/abs/2005.11401)
- **学科用法与实现**。维基词条用于核对通行术语。文档问答常把片段放入提示词，这是原定义的一种实现；切片方式、向量库和引用格式均属于实现选择。[维基百科，导言](https://en.wikipedia.org/wiki/Retrieval-augmented_generation) · [Anthropic，RAG 基本流程](https://www.anthropic.com/research/contextual-retrieval)
- **可追溯性**。检索结果可带原文和来源信息；生成环节可把主张关联到指定文档的页码、字符范围或内容块。由此推得，资料会修订时，还应保留可区分版本的标识，否则同一位置可能已换成新文字。定位后仍需核对原文是否支持主张。[阿里云，知识检索 · API 调用](https://help.aliyun.com/zh/model-studio/rag-knowledge-retrieval) · [Claude，引用位置](https://platform.claude.com/docs/en/build-with-claude/citations#citation-indices) · [Gao 等，引用质量评估](https://aclanthology.org/2023.emnlp-main.398/)

## 建库、查询与使用场景 · A02

- **更新与权限**。有些服务异步建立索引，删除后也可能短暂命中旧片段。排查时比较源文档、索引状态、实际返回的文档标识和模型输入。权限检查以请求者身份为准，先限定可查资料；魔笔给出按权限组映射到知识库的实现，粒度是知识库。[OpenAI，向量库文件操作](https://developers.openai.com/api/docs/guides/retrieval#vector-store-file-operations) · [阿里云，检索范围 · 方案概览](https://help.aliyun.com/zh/mobi/control-knowledge-base-retrieval-scope)
- **全文与检索**。授权资料能放入上下文时，可以全文输入作基线，实测回答质量、耗时和成本。资料过长时要选择证据；即使放得下，证据位置也可能影响利用效果。具体长度界限随模型和任务而变。[Anthropic，直接使用较长提示词](https://www.anthropic.com/research/contextual-retrieval) · [Liu 等，长上下文多文档问答](https://aclanthology.org/2024.tacl-1.9/)

## 分类与瓶颈 · A03、A04

- **检索依据和时机**。词项匹配适合保留编号等字面线索，向量相似度可以联系不同措辞，两路候选可融合去重。若后续信息需求取决于前文，可以再发起查询；主动检索论文以长文本生成为实验设定，用低置信度触发补查只是其中一种策略。[Anthropic，RAG 基本流程](https://www.anthropic.com/research/contextual-retrieval) · [Jiang 等，主动检索](https://aclanthology.org/2023.emnlp-main.495/)
- **证据丢失的位置**。孤立片段可能缺少主语或标题，可在建索引时补入文档上下文。重排只能处理已召回的候选；扩大候选数会影响重排开销，扩大最终输入还会带入干扰文字。定位时逐一核对源文、候选、实际输入是否保有必要条件，再判断模型是否用对证据。没有通用的最佳片长或返回数量。[Anthropic，上下文检索、重排及其成本](https://www.anthropic.com/research/contextual-retrieval) · [阿里云，知识库独立配置与检索流程](https://help.aliyun.com/zh/model-studio/rag-knowledge-retrieval) · [Liu 等，证据位置实验](https://aclanthology.org/2024.tacl-1.9/)

## 评估与验证 · A05

- **检索口径**。在有已标注证据的问题中，逐题判断前 k 个片段有没有命中，再对题目取平均。若一题需要多条证据，则另算找回的必要证据数占所需总数的比例。标注时约定片段或事实为计数单位，认可可互相替代的完整证据组合。资料不足题单列。[Ragas，按标识计算上下文召回率](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_recall/#id-basedcontext-recall) · [KILT，第 3 节检索评估](https://aclanthology.org/2021.naacl-main.200.pdf#page=7)
- **回答口径**。正确性与可信参考答案对照，忠实度逐项核对回答中的事实是否有输入资料支持。只有在指定版本与访问范围内资料不足、且任务要求依据资料作答时，才把说明证据不足列为预期行为。分别记录无依据作答和有依据却拒答的比例。[Ragas，忠实度](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/) · [Gao 等，正确性与引用质量](https://aclanthology.org/2023.emnlp-main.398/) · [RAG-RewardBench，资料不足时的标注指南](https://aclanthology.org/2025.findings-acl.877.pdf)
- **对照设计**。Liu 等对同一组题比较过无文档和仅给含答案文档的表现。本提纲在可回答题上加入实际检索组：与无资料组比较，观察采用检索后的净变化；与人工证据组比较，检查证据选择和呈现还有多少改善空间。两组差距同时受证据完整性、干扰文字和排列位置影响。进一步归因时，固定其他条件，只替换一个因素。人工组也答错时，复核参考答案、问题歧义和模型对证据的利用。各组用同一口径记录每题总耗时与费用。[Liu 等，第 2.3、5 节](https://arxiv.org/html/2307.03172v3#S2.SS3)

**实测才能确定的事项**：具体知识库的更新延迟、片长、候选数、重排收益及拒答阈值取决于数据、模型与任务目标。提纲保留选择方法与验证条件。

## 核心价值补核

本节按知识更新、业务知识接入、事实依据、大资料库检索、引用核验五个问题组织，属于本文的教学归纳。

- 原始论文第 1 节说明参数知识难以修改、生成可能有事实错误、依据难以检查。第 4.5 节用不同时期索引验证知识更新，第 4.2—4.3 节报告特定任务上的事实性改善。效果受实验设定限制。[原始论文全文](https://arxiv.org/html/2005.11401v4)
- Anthropic 文首讨论业务背景知识，“RAG 基本流程”解释资料库超过上下文容量时的检索用途。输入量降低能否转化为总成本降低，还需计入检索、索引和重排开销。[上下文检索](https://www.anthropic.com/research/contextual-retrieval)
- 引用评估研究区分回答正确性和引用质量。保留出处提供核验入口，引用是否真正支持主张仍须检验。[引用评估论文](https://aclanthology.org/2023.emnlp-main.398/)

## 针对核心价值的独立检索

本轮以“为什么使用 RAG”“RAG 的收益与限制”为检索问题，新增阅读 AWS 与 Google Cloud 官方说明。

- AWS 的“为何重要”列出信息过时、回答过于泛化、事实错误、来源不可靠与术语混淆。“收益”列出接入新资料的成本、时效性、引用核验和开发者对资料来源的控制。由此补充上一版遗漏的知识维护与来源选择价值。[AWS，RAG 的必要性与收益](https://aws.amazon.com/what-is/retrieval-augmented-generation/)
- Google Cloud 的“为何使用”强调新知识、事实依据及业务相关性，也解释检索如何帮助使用超出单次输入容量的资料。页面同时指出检索无关时，生成仍可能错误或偏题。[Google Cloud，为什么使用 RAG](https://cloud.google.com/use-cases/retrieval-augmented-generation)
- 教学归纳可围绕知识覆盖、事实依据、出处核验、知识维护四项展开。大型知识库的按需检索支撑这些能力。维护外部资料仍需更新索引，总成本和准确性应由实际评估决定。

## 工作原理 · 检索技术补核

DPR 的第 3.1—3.2 节说明双编码器分别表示问题和段落，并用正、负段落训练相似度排序。文档可预先编码建立索引，查询时编码问题并寻找匹配片段。该研究支撑“向量匹配能力来自训练”的解释，实际检索质量仍取决于任务与数据。[DPR 原文](https://aclanthology.org/2020.emnlp-main.550.pdf#page=2)

RAG 原始论文第 2.1 节将检索概率与给定文档的生成概率结合，第 2.3 节说明将问题和文档拼接给生成模型。正文据此说明外部资料参与生成，保留原论文机制与常见文档问答实现的具体语境。[RAG 原文](https://arxiv.org/html/2005.11401v4#S2.SS1)

## 分类 · 维度补核

独立检索 RAG 分类，补读 Gao 等综述第 II 节。作者按演进范式归纳 Naive、Advanced、Modular RAG：基本检索生成、检索前后优化、可组合模块与灵活流程。该分法属于作者的综述框架，不宜当作互斥且穷尽的统一标准。正文将其作为系统设计视角，并与检索匹配方式、检索轮次分别介绍；重点展开关键词、向量和混合检索，以衔接 A03 的选择问题。[Gao 等，第 II 节](https://arxiv.org/html/2312.10997v5#S2)

重新核对 Anthropic 的 RAG 基本流程与重排段落：BM25 依赖词项匹配，向量检索依赖表示相似度；两路候选可融合去重，重排是随后可选的步骤。全文没有提供混合检索对所有任务均优的保证，正文保留任务验证条件。[Anthropic，原文](https://www.anthropic.com/research/contextual-retrieval)

## 问题空间与方案 · 本轮核查

- 组织为片段语境、证据覆盖与处理成本、证据利用三类困难。Anthropic 的 The context conundrum / Implementing Contextual Retrieval 支持切分可能丢失语境及补充语境说明的机制；并不支持“片段越短越容易检索细节”的普遍规律。
- 阿里云知识检索的“知识库独立配置”“检索流程”分别设置初步候选和最终返回数量，支持候选与模型输入分开讨论。重排只能作用于已有候选。
- Liu 等第 2.3、5 节支持上下文位置与无关内容影响所测模型，不推广为所有模型上的固定表现。ALCE 区分答案正确性与引用质量，不将附引用视为正确性保证。
- 方案代价与选择条件是基于上述机制的教学归纳，未声明通用最优参数。

出处：[Anthropic](https://www.anthropic.com/research/contextual-retrieval) · [阿里云](https://help.aliyun.com/zh/model-studio/rag-knowledge-retrieval) · [Liu 等](https://arxiv.org/html/2307.03172v3#S2.SS3) · [ALCE](https://aclanthology.org/2023.emnlp-main.398/)
