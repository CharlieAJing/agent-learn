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

## 演进与瓶颈 · 章节重构

- 用户批准将“问题空间与方案”重构为“演进与瓶颈”，子节为“关键演进”“当前瓶颈”。A04 改为区分扩大单轮候选与多轮检索，旧排查题由新问题替代。其余章节保留，仅同步工作原理中的章节指引。
- 历史选取2020 Lewis RAG（第2、4.5节）、2023 Trivedi 交替检索与推理（第1—2节、Limitations）、2024 Anthropic Contextual Retrieval。是可组合的代表性路线，不宣称首次发明、统一升级阶段或穷尽发展史。
- 独立核查新增 ICLR 2025 Sufficient Context：第3节的充分性不等于真实性；第4节区分资料不足与模型利用问题；第5.1节把充分性和置信信号结合以做选择性作答，比较正确率与回答覆盖率。实验只支持所测模型/任务，不泛化到所有2026模型。
- 多轮检索依赖中间线索时才有针对性；重排与生成总成本需共同计算。资料库无依据不能笼统归因于漏检。当前瓶颈均按任务条件表述。

出处：[Lewis](https://arxiv.org/html/2005.11401v4#S4.SS5) · [Trivedi](https://aclanthology.org/2023.acl-long.557.pdf) · [Anthropic](https://www.anthropic.com/research/contextual-retrieval) · [Joren](https://proceedings.iclr.cc/paper_files/paper/2025/file/33dffa2e3d2ab74a783d1a8c292f66d9-Paper-Conference.pdf)

备选来源经核查未纳入本节，以控制范围：RAMDocs 2025区分歧义与错误/噪声；GRAB-RAG 2026只评估窄范围冻结小模型，不足以断言整个领域现状。

## 关键演进 · 按新筛选规则重写

结合 Gao 综述第 I、II、V 节与原始研究，按知识来源、资料接入、流程控制三项设计变化归纳；不宣称唯一共识阶段。原有片段补语境保留在当前瓶颈，不再作为同等层级主线。新增阅读 Ram 等 In-Context RALM（TACL 2023）第1—2节：冻结生成模型并将检索文本前置，实验主要为语言建模，不声称直接证明所有问答任务收益。新增 Self-RAG 原始论文（ICLR 2024，2023预印本）第3节：专门训练反思标记以控制检索、评价相关性与支持度；不将该模型描述成无需训练或完美自检。

出处：[综述](https://arxiv.org/html/2312.10997v5) · [Ram](https://aclanthology.org/2023.tacl-1.75.pdf) · [Self-RAG](https://proceedings.iclr.cc/paper_files/paper/2024/file/25f7be9694d7b32d5cc670927b8091e1-Paper-Conference.pdf)

## 使用场景 · 提炼关键条件

- 依据已读 AWS 的外部知识、知识更新、来源标注及检索章节，与 Anthropic 的业务背景、长提示词、RAG 基本流程和片段局限，归纳三个条件：作答需外部依据、依据可按问题查找、找到资料后仍需解释或整合。这是本文的教学推导，不是来源给出的统一分类或充分保证。
- 资料量大且单次仅需部分内容，增强按需检索的价值；全文输入适用于范围确定、输入容量与开销允许的文档任务。只定位原文可止于搜索。完整统计或检查需要覆盖保障，少量片段不足；不由此否定结合全量查询或遍历的 RAG 系统。
- 专题资料整理属于根据检索与生成机制推得的用法，不声称实验验证了全面综述效果。权限与引用是配套要求，不单独作为选用 RAG 的充分理由。本次按用户要求不执行审稿。

出处：[AWS，RAG 说明](https://aws.amazon.com/what-is/retrieval-augmented-generation/) · [Anthropic，上下文检索](https://www.anthropic.com/research/contextual-retrieval)

## 能力模型 · 中文因子与作用关系

- 依据最新提示重写“能力模型”，公式、正文与表格直接使用中文因子名。本轮由主 Agent 对成稿评分，不启动完整审稿流程；其他正文章节保留。
- “有据作答成功率 = 依据充分率 × 依据利用成功率”是本文按任务目标所作的条件概率分解，不是论文原式。依据利用成功率仅在依据充分的问题中统计，不要求独立；无资料支持但凭记忆答对、合理拒答另评。
- “依据充分率 = 知识源覆盖率 × 检索找齐率 × 上下文保留率”限于依据仅沿知识源、候选、最终输入筛选传递的流程。后续比例以前一步成功为条件，完整指至少一组足以作答的有效依据。
- 保留 Joren 等第 3—4 节关于充分性与作答结果的边界；本节的充分有效依据比论文自动充分性标签更严格，要求事实适用且有效。
- 回读 Chen 等信息整合实验、错误分析及噪声实验：所测模型出现遗漏、事实合并和对象错配，复杂整合任务更易受干扰。正文由此提出“单项正确而整合错误时考察整合”“依据齐全后验证减少干扰”的候选判断，不声称这些干预已在用户任务中实证有效。
- 回读 Liu 等第 2.3 节：保留必要文档而调整位置可改变所测模型的表现。该证据直接支持排序影响，不直接证明按问题分组必然有效；正文把调整排序或分组写成保持依据不变后的验证方向。
- 回读 Anthropic 的片段上下文、输入数量、重排与代价段落：保留上下文可能兼顾检索和理解；更多输入的覆盖收益与干扰代价需合并观察。不把其检索改进实验当作生成质量改进的普遍保证。
- 删除未说明具体作用的字母函数表达。改以模型能力与任务要求、资料干扰、输入组织的关系说明依据利用。杠杆判断来自条件关系与可干预性，不将“因子最低”直接当作最佳改动；保持其他因子不变仅作敏感性推断前提，实际结果以同一组任务对照验证。

出处：[Joren 等，第 3—4 节](https://arxiv.org/html/2411.06037v2#S3) · [Chen 等，信息整合及错误分析](https://arxiv.org/html/2309.01431v2) · [Liu 等，第 2.3 节](https://arxiv.org/html/2307.03172v3#S2.SS3) · [Anthropic，上下文检索](https://www.anthropic.com/research/contextual-retrieval)

## 本轮覆盖提纲与取证

保留原六章及 A01–A05 的考查目标。概念界定检索在生成中的作用；工作原理追踪证据从原文到输入的去向；分类区分匹配方式与检索轮次；演进解释引入多轮的条件；使用场景判断任务需要局部还是全量证据；评估用人工证据对照定位损失。追加题覆盖条件分母、全量任务与合理拒答。

- [原始论文第 2.1—2.4 节](https://arxiv.org/html/2005.11401v4#S2)给出按文档加权的生成机制。将原论文与工程中的片段拼接分开解释。
- [上下文充分性，第 3—5 节](https://arxiv.org/html/2411.06037v2#S3)区分相关、充分与模型作答。正文的条件比例是用于诊断的自定义口径。
- [多步检索研究](https://aclanthology.org/2023.acl-long.557/)用中间线索引导下一轮检索。结论限于有信息依赖的任务。
- [上下文检索实验](https://www.anthropic.com/research/contextual-retrieval)考察补全片段语境和重排。检索实验不直接证明最终答案正确。
- 提纲自查重点：使用场景需覆盖穷举要求，评估需分开记录有据答对与合理拒答。保留模板提示供后续审稿；本轮不执行完整审稿。

### 本轮出处与目录去向

- [OpenAI，检索与排序](https://developers.openai.com/api/docs/guides/retrieval)与[阿里云，建立评估基线](https://help.aliyun.com/zh/model-studio/rag-optimization/)支持区分候选、重排和最终输入。服务默认切分长度不作为通则。
- [Liu 等，位置对照实验](https://aclanthology.org/2024.tacl-1.9.pdf)支持在材料不变时改变顺序，不推断所有模型存在相同的位置偏好。
- 沿用六章。资料准备与检索作答的细分标题并入基本过程图和关键组成；能力模型的子标题合入能力模型、当前瓶颈和干预与验证；使用场景增设 Ask。分类保留匹配方式与检索轮次，整体设计的变化移至关键演进。
