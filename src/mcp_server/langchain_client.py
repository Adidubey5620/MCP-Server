import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.mcp import MCPAdapter
from langchain.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.prebuilt import create_react_agent

load_dotenv()

llm = ChatOpenAI(
    model="baidu/ernie-5.5-flash-preview:free",
    openai_api_key=os.environ["OPENROUTER_API_KEY"],
    openai_api_base="https://openrouter.ai/api/v1",
)

mcp_adapter = MCPAdapter("http://127.0.0.1:8000/mcp")

THREAD_ID = "main-session"
DB_PATH = str(Path(__file__).resolve().parents[2] / "checkpoints.db")

async def main():

    async with mcp_adapter:
        tools = await mcp_adapter.list_tools()

        for tool in tools:
            print(f"tool's name: {tool.name} tool's description: {tool.description}")

        agent = create_agent(
            model=llm,
            tools=tools,
            system_prompt="you are a helpful task management assistant"
        )

        result = await agent.ainvoke({"messages" : [HumanMessage(content="Find the task titled 'Prepare MCP Demo Slides' in my database and change its status to 'in_progress'. " \
        "Then retrieve the tasks again to verify the change. Do not create any new tasks.")]})

        for message in result["messages"]:
            for tool_call in getattr(message, "tool_calls", []):
                print("Tool called:", tool_call["name"])
                print("Arguments:", tool_call["args"])

        print(result["messages"][-1].content)

async def main2():

    async with AsyncSqliteSaver.from_conn_string(DB_PATH) as checkpointer:
        async with mcp_adapter:
            tools = await mcp_adapter.list_tools()

            agent = create_react_agent(
                model=llm,
                tools=tools,
                prompt="you are a helpful task management assistant",
                checkpointer=checkpointer
            )

            config = {"configurable": {"thread_id": THREAD_ID}}
            human_question = input("please ask your question or type q to exit:\n")

            while human_question != "q":

                result = await agent.ainvoke({"messages": [HumanMessage(content=human_question)]}, config=config)

                print(result["messages"][-1].content)

                human_question = input("please ask your question or type q to exit:\n")


if __name__ == "__main__":
    asyncio.run(main2())
