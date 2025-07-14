from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import base64
import os
load_dotenv()

async def describe_image(tmp_name: str):
    llm = ChatOpenAI(model=os.getenv("IMAGE_MODEL"), temperature=0)
    with open(tmp_name, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")
    response = await llm.ainvoke([HumanMessage(
                content=[
                    {"type": "text", "text": "Please analyze this image."},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}
                    },
                ]
            )
        ]
    )
    return response.content