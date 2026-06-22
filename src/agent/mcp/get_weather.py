
from langchain_tavily import TavilySearch
from fastmcp import FastMCP

mcp = FastMCP("get_weather")

tavily = TavilySearch(
    max_results=1,
    topic="general",          # general/news/finance
    include_answer=False,
    include_raw_content=False,
)


@mcp.tool(description="联网搜索指定城市的天气，以消息字符串的形式返回")
def get_weather(city: str) -> str:
    # 使用TavilySearch进行联网搜索
    resp = tavily.invoke({"query": f"{city} 天气"})
    results = (resp or {}).get("results") or []
    if not results:
        return "未找到相关天气信息"

    top = results[0]
    title = top.get("title", "")
    url = top.get("url", "")
    snippet = top.get("content", "")
    return f"{title}\n{url}\n{snippet}".strip()

mcp.run(transport="http")