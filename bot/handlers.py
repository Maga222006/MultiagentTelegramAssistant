from aiogram.types import Message, FSInputFile
from agent.text_to_speech import voice
from agent.multi_agent import call_multi_agent_system
from bot.keyboards import get_main_keyboard
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
    await msg.bot.send_chat_action(chat_id=msg.from_user.id, action=ChatAction.UPLOAD_VOICE)
    file = await msg.bot.get_file(msg.voice.file_id)
    file_url = f"https://api.telegram.org/file/bot{msg.bot.token}/{file.file_path}"
    state = {
        "user_id": str(msg.from_user.id),
        "first_name": msg.from_user.first_name,
        "last_name": msg.from_user.last_name,
        "file_url": file_url,
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
        modality="voice"
    )
    await msg.bot.send_chat_action(chat_id=msg.from_user.id, action=ChatAction.TYPING)
    await message.edit_text(response['messages'][-1]['content'])
    await msg.bot.send_chat_action(chat_id=msg.from_user.id, action=ChatAction.RECORD_VOICE)
    file_name = uuid.uuid4()
    await voice(query=response['messages'][-1]['content'], file_name=f"mediafiles/{file_name}.wav")
    voice_file = FSInputFile(f"mediafiles/{file_name}.wav")
    await msg.answer_voice(voice_file)
    os.remove(f'mediafiles/{file_name}.wav')


@router.message(F.document)
async def document_handler(msg: Message):
    await msg.bot.send_chat_action(chat_id=msg.from_user.id, action=ChatAction.UPLOAD_DOCUMENT)
    file = await msg.bot.get_file(msg.document.file_id)
    file_url = f"https://api.telegram.org/file/bot{msg.bot.token}/{file.file_path}"
    state = {
        "user_id": str(msg.from_user.id),
        "message": {"role": "user", "content": msg.text or ""},
        "first_name": msg.from_user.first_name,
        "last_name": msg.from_user.last_name,
        "file_url": file_url,
    }
    message = await msg.answer(random.choice([
        "On it...",
        "Processing your file...",
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
        modality="file"
    )
    await msg.bot.send_chat_action(chat_id=msg.from_user.id, action=ChatAction.TYPING)
    await message.edit_text(response["messages"][-1]["content"])


@router.message(F.photo)
async def photo_handler(msg: Message):
    await msg.bot.send_chat_action(chat_id=msg.from_user.id, action=ChatAction.UPLOAD_PHOTO)
    file = await msg.bot.get_file(msg.photo[-1].file_id)
    file_url = f"https://api.telegram.org/file/bot{msg.bot.token}/{file.file_path}"
    state = {
        "user_id": str(msg.from_user.id),
        "message": {"role": "user", "content": msg.text or ""},
        "first_name": msg.from_user.first_name,
        "last_name": msg.from_user.last_name,
        "file_url": file_url,
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
        modality="image"
    )
    await msg.bot.send_chat_action(chat_id=msg.from_user.id, action=ChatAction.TYPING)
    await message.edit_text(response['messages'][-1]['content'])


@router.message(F.text)
async def chat_handler(msg: Message):
    state = {
        "user_id": str(msg.from_user.id),
        "message": {"role": "user", "content": msg.text},
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
    await message.edit_text(response['messages'][-1]['content'])


