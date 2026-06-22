# cs599-project

# 扫地机器人智能客服 Agent 系统

## 项目简介

面向扫地/扫拖一体机器人用户的智能客服 AI Agent 系统。基于 ReAct 推理模式，整合 RAG 知识库检索、MCP 外部服务调用、用户数据分析等多种能力，为用户提供专业的产品咨询、使用指导、故障排查及个性化使用报告生成服务。

## 方向

**方向一：Agentic AI 原生开发**

## 技术栈

| 类别 | 技术选型 |
|------|----------|
| AI IDE | VS Code + Claude Code |
| LLM | 阿里通义千问 qwen3-max（ChatTongyi） |
| Embedding | DashScope text-embedding-v4 |
| Agent 框架 | LangGraph + LangChain |
| 向量数据库 | Chroma |
| 协议 | MCP（FastMCP + langchain-mcp-adapters） |
| 日志 | Python logging（控制台 + 文件双通道） |
| 环境管理 | Conda (rag) |

## 目录结构

```
.
├── agent/                      # Agent 核心
│   ├── react_agent.py          # ReAct Agent 主入口，流式输出
│   ├── mcp/
│   │   └── get_weather.py      # MCP 天气服务（FastMCP HTTP 服务）
│   └── tools/
│       ├── agent_tools.py      # 工具定义（6 个 @tool 工具函数）
│       └── middleware.py       # Agent 中间件（监控、日志、动态提示词）
├── config/                     # YAML 配置文件
│   ├── agent.yml               # Agent 参数（外部数据路径）
│   ├── chroma.yml              # 向量库参数（分块、检索配置）
│   ├── prompt.yml              # 提示词文件路径
│   └── rag.yml                 # 模型名称配置
├── data/                       # 知识库源文件
│   ├── 扫地机器人100问.pdf
│   ├── 扫地机器人100问2.txt
│   ├── 扫拖一体机器人100问.txt
│   ├── 选购指南.txt
│   ├── 故障排除.txt
│   ├── 维护保养.txt
│   └── external/
│       └── records.csv         # 用户使用记录数据
├── docs/                       # 项目文档
│   └── CS599_大作业报告.pdf      # 课程大作业报告
├── prompts/                    # 提示词模板
│   ├── main_prompt.txt         # 默认系统提示词
│   ├── report_prompt.txt       # 报告生成提示词
│   └── rag_summarize.txt       # RAG 摘要提示词
├── rag/                        # RAG 检索增强生成
│   ├── vector_store.py         # Chroma 向量存储（MD5 去重）
│   └── rag_service.py          # RAG 摘要服务
├── utils/                      # 工具模块
│   ├── config_handler.py       # YAML 配置加载器
│   ├── file_handler.py         # 文件加载 + MD5 计算
│   ├── logger_handler.py       # 日志配置
│   ├── path_tool.py            # 项目路径解析
│   └── prompt_loader.py        # 提示词文件加载
├── model/
│   └── factory.py              # 模型工厂（ChatModel + Embedding）
└── logs/                       # 运行日志
```

## 环境搭建

### 1. 依赖安装

```bash
pip install langchain langchain-community langchain-chroma langchain-text-splitters \
            langchain-tavily langchain-mcp-adapters fastmcp pyyaml weasyprint
```

### 2. 环境变量配置

项目所需的 API Key 通过环境变量配置，**严禁硬编码**：

```bash
export DASHSCOPE_API_KEY="your-dashscope-api-key"   # 通义千问 LLM + Embedding
export TAVILY_API_KEY="your-tavily-api-key"         # MCP 天气搜索
```

### 3. 启动步骤

**Step 1：构建知识库**

```bash
PYTHONPATH=. python rag/vector_store.py
```

**Step 2：启动 MCP 天气服务**（新终端）

```bash
python agent/mcp/get_weather.py
```

**Step 3：启动 Agent**

```bash
PYTHONPATH=. python agent/react_agent.py
```

> **注意**：所有命令需在项目根目录下执行，且需设置 `PYTHONPATH=.` 确保模块导入正确。

## 项目状态

- [√] Proposal（设计文档 + 架构图 + Spec 初稿）
- [√] MVP（核心闭环 Demo：ReAct 推理 + RAG + MCP + 报告生成）
- [√] Final（完整文档 + 代码 + 报告）

## 开源项目：
基于黑马程序扫地机器人客服agent，添加mcp，多agent等功能
