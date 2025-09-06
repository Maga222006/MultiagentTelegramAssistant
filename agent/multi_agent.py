from langchain_core.messages import AnyMessage
from typing import TypedDict, Literal
import httpx
import json
import os

class State(TypedDict):
    message: AnyMessage
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
    model_api_key: str
    model: str
    clear_history: bool
    messages: list


async def call_multi_agent_system(
    state: State,
    modality: Literal["text", "voice", "image", "file", "authorzation"] = "text",
    file_name: str = None,
    file_path: str = None
):
    url = f"{os.getenv('BASE_URL')}/{modality}"

    async with httpx.AsyncClient() as client:
        if modality in ["text", "authorization"]:
            response = await client.post(
                url=url,
                data={"state": json.dumps(state)},
                timeout=5000
            )
        else:
            with open(file_path, "rb") as file:
                response = await client.post(
                    url=url,
                    data={"state": json.dumps(state)},
                    files={"file": (file_name, file)},
                    timeout=5000
                )

    response.raise_for_status()
    return response.json()