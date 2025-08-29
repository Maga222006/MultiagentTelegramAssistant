from langchain_core.messages import AnyMessage
from typing import TypedDict, Literal
import httpx
import json
import os

class State(TypedDict):
    message: AnyMessage
    file_url: str
    user_id: str
    first_name: str
    last_name: str
    assistant_name: str
    latitude: str
    longitude: str
    location: str
    openweathermap_api_key: str
    github_token: str
    tavily_api_key: str
    openai_api_key: str
    openai_api_base: str
    model: str
    spare_model: str
    stt_model: str
    clear_history: bool
    messages: list


async def call_multi_agent_system(
    state: State,
    modality: Literal["text", "voice", "image", "file", "authorzation"] = "text",
):
    url = f"{os.getenv('BASE_URL')}/{modality}"
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=url,
            data={"state": json.dumps(state)},
            timeout=5000
        )
    response.raise_for_status()
    return response.json()