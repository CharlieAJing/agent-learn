# 资料检索

## 策略

- 多来源检索时，优先使用 subagent 完成搜索、阅读与证据整理；主 Agent 负责确定检索目标、整合结果，并对关键或存疑结论回源核验。简单检索由主 Agent 直接完成。
- 使用必搜，并围绕主题和证据缺口自主扩展搜索，按证据质量取舍资料。
- 围绕关键问题独立检索，初稿中的观点作为待验证的假设。检索结果需指出已有观点的依据、遗漏和需要修正之处；主 Agent 据此调整提纲。
- 按需交叉核验，依据充分即停止。

## 子任务输入与返回

- **输入**：主 Agent 提供检索目标、必要背景和规范路径；子 Agent 使用独立上下文启动（`fork_turns: "none"`），避免复制整段聊天历史。
- **返回**：仅回传关键结论、适用条件、出处定位（链接与章节）、冲突或缺口；必要时附短摘录，不回传整页原文与完整检索过程。

## 必搜
- [Wikipedia（维基百科）](https://en.wikipedia.org/wiki/Main_Page)
- [Claude 文档](https://platform.claude.com/docs/en/intro)
- [OpenAI 文档](https://developers.openai.com/api/docs)
- [阿里云文档](https://help.aliyun.com/zh/)
