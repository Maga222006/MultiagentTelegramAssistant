from gtts import gTTS
import regex as re
import asyncio

async def voice(query: str, file_name: str):
    loop = asyncio.get_event_loop()

    def save():
        text = re.sub(r'[^\p{L}\p{N}\s+\-/=<>^%(),.!]', '', query)
        tts = gTTS(text=text, lang="en")
        tts.save(file_name)

    await loop.run_in_executor(None, save)