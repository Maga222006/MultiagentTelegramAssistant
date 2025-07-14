from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
load_dotenv()

client = AsyncOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY")
)

async def transcribe(file_name):
    transcription = await client.audio.transcriptions.create(
        model=os.getenv("STT_MODEL"),
        file=open(file_name, "rb")
    )
    return transcription