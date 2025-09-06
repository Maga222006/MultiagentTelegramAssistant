from aiogram.types import Message, FSInputFile
from agent.text_to_speech import voice
from agent.multi_agent import call_multi_agent_system
from bot.keyboards import get_main_keyboard
from aiogram.enums import ParseMode
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram import Router, F
import random
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
    state = {
        "user_id": str(msg.from_user.id),
        "first_name": msg.from_user.first_name,
        "last_name": msg.from_user.last_name,
        "latitude": msg.location.latitude,
        "longitude": msg.location.longitude,
    }
    await msg.answer("📍 Location Updated! You're all set.")
    await call_multi_agent_system(state=state, modality="authorization")

@router.message(F.voice)
async def voice_handler(msg: Message):
    state = {
        "user_id": str(msg.from_user.id),
        "first_name": msg.from_user.first_name,
        "last_name": msg.from_user.last_name,
    }
    await msg.bot.send_chat_action(chat_id=msg.from_user.id, action=ChatAction.UPLOAD_VOICE)
    file = await msg.bot.get_file(msg.voice.file_id)
    file_path = file.file_path
    print(file_path)
    file_name = uuid.uuid4()
    await msg.bot.download_file(file_path, f'mediafiles/{file_name}.ogg')
    message = await msg.answer(random.choice([
        "On it...",
        "Processing your request...",
        "Got it, let me check...",
        "One moment, working on that...",
        "Looking into it...",
        "Just a sec...",
        "Gathering information...",
        "Hmm, let’s see...",
        "Hold on, almost there...",
        "Thinking..."
    ]))
    response = await call_multi_agent_system(
        state=state,
        modality="voice",
        file_path=f"mediafiles/{file_name}.ogg",
        file_name=f"{file_name}.ogg"
    )
    await msg.bot.send_chat_action(chat_id=msg.from_user.id, action=ChatAction.TYPING)
    await message.edit_text(response['messages'][-1]['content'])
    await msg.bot.send_chat_action(chat_id=msg.from_user.id, action=ChatAction.RECORD_VOICE)
    await voice(query=response['messages'][-1]['content'], file_name=f"mediafiles/{file_name}.wav")
    voice_file = FSInputFile(f"mediafiles/{file_name}.wav")
    await msg.answer_voice(voice_file)
    os.remove(f'mediafiles/{file_name}.ogg')
    os.remove(f'mediafiles/{file_name}.wav')

@router.message(F.photo)
async def photo_handler(msg: Message):
    state = {
        "message": {"role": "user", "content": msg.text},
        "user_id": str(msg.from_user.id),
        "first_name": msg.from_user.first_name,
        "last_name": msg.from_user.last_name,
    }
    message = await msg.answer(random.choice([
        "On it...",
        "Processing your request...",
        "Got it, let me check...",
        "One moment, working on that...",
        "Looking into it...",
        "Just a sec...",
        "Gathering information...",
        "Hmm, let’s see...",
        "Hold on, almost there...",
        "Thinking..."
    ]))
    await msg.bot.send_chat_action(chat_id=msg.from_user.id, action=ChatAction.UPLOAD_PHOTO)
    file = await msg.bot.get_file(msg.photo[-1].file_id)
    file_path = file.file_path
    print(file_path)
    file_name = f"{uuid.uuid4()}.jpg"
    file_path_ = f"mediafiles/{file_name}"
    await msg.bot.download_file(file_path, file_path_)
    response = await call_multi_agent_system(
        state=state,
        modality="image",
        file_path=file_path_,
        file_name=file_name
    )
    await msg.bot.send_chat_action(chat_id=msg.from_user.id, action=ChatAction.TYPING)
    await message.edit_text(response['messages'][-1]['content'])
    os.remove(file_path_)

@router.message(F.document)
async def document_handler(msg: Message):
    state = {
        "message": {"role": "user", "content": msg.text},
        "user_id": str(msg.from_user.id),
        "first_name": msg.from_user.first_name,
        "last_name": msg.from_user.last_name,
    }
    message = await msg.answer(random.choice([
        "On it...",
        "Processing your request...",
        "Got it, let me check...",
        "One moment, working on that...",
        "Looking into it...",
        "Just a sec...",
        "Gathering information...",
        "Hmm, let’s see...",
        "Hold on, almost there...",
        "Thinking..."
    ]))
    await msg.bot.send_chat_action(chat_id=msg.from_user.id, action=ChatAction.UPLOAD_DOCUMENT)
    file = await msg.bot.get_file(msg.document.file_id)
    file_path = file.file_path
    print(file_path)

    ext = os.path.splitext(file_path.split("?")[0])[1].lower()
    file_name = f"{uuid.uuid4()}{ext}"
    file_path_ = f"mediafiles/{file_name}"
    await msg.bot.download_file(file_path, file_path_)
    response = await call_multi_agent_system(
        state=state,
        modality="file",
        file_path=file_path_,
        file_name=file_name
    )
    await msg.bot.send_chat_action(chat_id=msg.from_user.id, action=ChatAction.TYPING)
    await message.edit_text(response['messages'][-1]['content'])
    os.remove(file_path_)

@router.message(F.text)
async def chat_handler(msg: Message):
    state = {
        "message": {"role": "user", "content": msg.text},
        "user_id": str(msg.from_user.id),
        "first_name": msg.from_user.first_name,
        "last_name": msg.from_user.last_name,
    }
    message = await msg.answer(random.choice([
        "On it...",
        "Processing your request...",
        "Got it, let me check...",
        "One moment, working on that...",
        "Looking into it...",
        "Just a sec...",
        "Gathering information...",
        "Hmm, let’s see...",
        "Hold on, almost there...",
        "Thinking..."
    ]))
    response = await call_multi_agent_system(
        state=state,
        modality="text"
    )
    await msg.bot.send_chat_action(chat_id=msg.from_user.id, action=ChatAction.TYPING)
    await message.edit_text(text=response['messages'][-1]['content'], parse_mode=ParseMode.MARKDOWN)