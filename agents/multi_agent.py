from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.messages.utils import count_tokens_approximately
from agents.tools import coding_tools, researcher_tools
from sqlalchemy.ext.asyncio import create_async_engine
from langchain_openai.chat_models import ChatOpenAI
from langgraph_supervisor import create_supervisor
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent
from langmem.short_term import SummarizationNode
from database.user import get_user_by_id
from config import DATABASE_URL
from dotenv import load_dotenv
from agents import tools
import os

load_dotenv()
engine = create_async_engine(
    DATABASE_URL,
    echo=False
)
llm = ChatOpenAI(model=os.getenv("MODEL"), temperature=0)

summarization_node = SummarizationNode(
    token_counter=count_tokens_approximately,
    model=llm,
    max_tokens=4000,
    max_summary_tokens=1000,
    output_messages_key="llm_input_messages",
)

coding_agent = create_react_agent(
    llm,
    tools=coding_tools,
    name="coding_agent",
    prompt="You can only generate code ... ALWAYS web_search before coding.",
    pre_model_hook=summarization_node
)

supervisor = create_supervisor(
    model=llm,
    tools=researcher_tools,
    agents=[coding_agent],
    prompt="You are a supervisor agent ... do one agent at a time.",
    add_handoff_back_messages=False,
    add_handoff_messages=False,
    output_mode="full_history",
    pre_model_hook=summarization_node
)

graph = supervisor.compile()

async def call_assistant(message, user_id: str):
    """Call multi-agent system"""
    user_info = await get_user_by_id(user_id=user_id)
    tools.user_id = user_id

    message_history = SQLChatMessageHistory(
        session_id=user_id,
        connection=engine,
        async_mode=True
    )
    await message_history.aadd_message(message)
    messages = await message_history.aget_messages()


    system_msg = SystemMessage(
        content=f"""
            You are an intelligent, helpful personal assistant built using a multi-agent system architecture. Your tools include web search, weather and time lookups, code execution, and GitHub integration. You work inside a Telegram interface and respond concisely, clearly, and informatively.

            The user you are assisting is:
            - **Name**: {user_info.get('first_name', 'Unknown') or 'Unknown'} {user_info.get('last_name', '') or ''}
            - **User ID**: {user_id}
            - **Location**: {user_info.get('location', 'Unknown') or 'Unknown'}
            - **Coordinates**: ({user_info.get('latitude', 'N/A') or 'N/A'}, {user_info.get('longitude', 'N/A') or 'N/A'})

            You may use their location when answering weather or time-related queries. If the location is unknown, you may ask the user to share it.

            Stay helpful, respectful, and relevant to the user's query.
        """.strip()
    )

    result = await graph.ainvoke(
        input={"messages": messages[:-1]+[system_msg, messages[-1]]},
        config={"configurable": {"thread_id": user_id}}
    )
    return result

