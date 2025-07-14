from langchain_core.messages import HumanMessage
from database.user import create_or_update_user
from aiogram.types import Message, FSInputFile
from database.config import load_config_to_env
from bot.keyboards import get_main_keyboard
from media.text_to_speech import voice
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram import Router, F
import uuid
import os

router = Router()
is_imported = False

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(
        "👋 Hi! Use the buttons below to configure your assistant or share your location.",
        reply_markup=get_main_keyboard()
    )

@router.message(F.location)
async def location_handler(msg: Message):
    await create_or_update_user(
        user_id=str(msg.from_user.id),
        first_name=msg.from_user.first_name,
        last_name=msg.from_user.last_name,
        latitude=msg.location.latitude,
        longitude=msg.location.longitude
    )
    await msg.answer("📍 Location Updated! You're all set.")

@router.message(F.voice)
async def voice_handler(msg: Message):
    global is_imported
    await load_config_to_env(user_id=str(msg.from_user.id))
    from agents.multi_agent import call_assistant
    from media.speech_to_text import transcribe
    file = await msg.bot.get_file(msg.voice.file_id)
    file_path = file.file_path
    file_name = uuid.uuid4()
    await msg.bot.download_file(file_path, f'{file_name}.ogg')
    transcribed_msg = await transcribe(f"{file_name}.ogg")
    response = await call_assistant(HumanMessage(content=transcribed_msg.text), str(msg.from_user.id))
    await msg.bot.send_chat_action(chat_id=msg.from_user.id, action=ChatAction.TYPING)
    await msg.answer(response['messages'][-1].content)
    await msg.bot.send_chat_action(chat_id=msg.from_user.id, action=ChatAction.RECORD_VOICE)
    await voice(query=response['messages'][-1].content, file_name=f"{file_name}.wav")
    voice_file = FSInputFile(f"{file_name}.wav")
    await msg.answer_voice(voice_file)
    os.remove(f'{file_name}.ogg')
    os.remove(f'{file_name}.wav')

@router.message(F.photo)
async def photo_handler(msg: Message):
    global is_imported
    await load_config_to_env(user_id=str(msg.from_user.id))
    from agents.multi_agent import call_assistant
    from media.image_processing import describe_image
    file = await msg.bot.get_file(msg.photo[-1].file_id)
    file_path = file.file_path
    tmp_name = f"{uuid.uuid4()}.jpg"
    await msg.bot.download_file(file_path, tmp_name)
    image_description = await describe_image(tmp_name)
    response = await call_assistant(HumanMessage(content=f"{msg.text} \nUploaded image description: {image_description}"), str(msg.from_user.id))
    await msg.bot.send_chat_action(chat_id=msg.from_user.id, action=ChatAction.TYPING)
    await msg.answer(response['messages'][-1].content)
    os.remove(tmp_name)

@router.message(F.text)
async def chat_handler(msg: Message):
    global is_imported
    await load_config_to_env(user_id=str(msg.from_user.id))
    from agents.multi_agent import call_assistant
    response = await call_assistant(message=HumanMessage(content=msg.text), user_id=str(msg.from_user.id))
    await msg.bot.send_chat_action(chat_id=msg.from_user.id, action=ChatAction.TYPING)
    await msg.answer(response['messages'][-1].content)
