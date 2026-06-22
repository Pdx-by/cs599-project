from langchain.agents import create_agent
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from model.factory import chat_model
from utils.prompt_loader import load_system_prompts
from agent.tools.agent_tools import (
    rag_summarize,
    get_user_location,
    get_user_id,
    get_current_month,
    fetch_external_data,
    fill_context_for_report,
)
from agent.tools.middleware import monitor_tool, log_before_model, report_prompt_switch


class ReactAgent:
    def __init__(self, agent):
        self.agent = agent

    @classmethod
    async def create(cls):
        client = MultiServerMCPClient(
            {
                "weather": {
                    "transport": "http",
                    "url": "http://localhost:8000/mcp",
                }
            }
        )
        mcp_tools = await client.get_tools()

        agent = create_agent(
            model=chat_model,
            system_prompt=load_system_prompts(),
            tools=[
                rag_summarize,
                get_user_location,
                get_user_id,
                get_current_month,
                fetch_external_data,
                fill_context_for_report,
                *mcp_tools,
            ],
            middleware=[monitor_tool, log_before_model, report_prompt_switch],
        )
        return cls(agent)

    async def execute_stream(self, query: str):
        def _normalize_content(content) -> str:
            if isinstance(content, str):
                return content.strip()

            if isinstance(content, list):
                parts = []
                for item in content:
                    if isinstance(item, str):
                        parts.append(item)
                    elif isinstance(item, dict):
                        text = item.get("text")
                        if isinstance(text, str):
                            parts.append(text)
                return "".join(parts).strip()

            return str(content).strip()

        input_dict = {
            "messages": [
                {"role": "user", "content": query},
            ]
        }

        async for chunk in self.agent.astream(input_dict, stream_mode="values", context={"report": False}):
            latest_message = chunk["messages"][-1]
            if latest_message.content:
                text = _normalize_content(latest_message.content)
                if text:
                    yield text + "\n"

async def main():
    agent = await ReactAgent.create()
    async for chunk in agent.execute_stream("生成使用报告"):
        print(chunk, end="", flush=True)
        
if __name__ == "__main__":
    asyncio.run(main())
