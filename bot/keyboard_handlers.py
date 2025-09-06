from agent.multi_agent import call_multi_agent_system
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router, F

router = Router()

class ConfigStates(StatesGroup):
    groq_api_key = State()
    weather_key = State()
    github_token = State()
    tavily_key = State()
    assistant_name = State()

@router.message(F.text == "🔑 Set Groq API Key")
async def ask_groq_api_key(msg: Message, state: FSMContext):
    await msg.answer("Please send your Groq API Key:")
    await state.set_state(ConfigStates.groq_api_key)

@router.message(F.text == "🤖 Set Assistant Name")
async def ask_name(msg: Message, state: FSMContext):
    await msg.answer("Please send your Assistant Name:")
    await state.set_state(ConfigStates.assistant_name)

@router.message(F.text == "☁️ Set OpenWeatherMap Key")
async def ask_weather_key(msg: Message, state: FSMContext):
    await msg.answer("Please enter your OpenWeatherMap API key:")
    await state.set_state(ConfigStates.weather_key)

@router.message(F.text == "💙 Set GitHub Token")
async def ask_github_token(msg: Message, state: FSMContext):
    await msg.answer("Please enter your GitHub token:")
    await state.set_state(ConfigStates.github_token)

@router.message(F.text == "🔍 Set Tavily API Key")
async def ask_tavily_key(msg: Message, state: FSMContext):
    await msg.answer("Please enter your Tavily API key:")
    await state.set_state(ConfigStates.tavily_key)

@router.message(F.text == "💾 Clear Chat History")
async def clear_chat_history(msg: Message, state: FSMContext):
    state_ = {
        "user_id": str(msg.from_user.id),
        "first_name": msg.from_user.first_name,
        "last_name": msg.from_user.last_name,
        "clear_history": True
    }
    await msg.answer("✅ Assistant's chat history cleared.")
    await call_multi_agent_system(state=state_, modality="authorization")


# Handlers to save inputs
@router.message(F.text, ConfigStates.groq_api_key)
async def save_groq_api_key(msg: Message, state: FSMContext):
    state_ = {
        "user_id": str(msg.from_user.id),
        "first_name": msg.from_user.first_name,
        "last_name": msg.from_user.last_name,
        "groq_api_key": msg.text
    }
    await msg.answer("✅Groq API Key saved.")
    await state.clear()
    await call_multi_agent_system(state=state_, modality="authorization")


@router.message(F.text, ConfigStates.assistant_name)
async def save_assistant_name(msg: Message, state: FSMContext):
    state_ = {
        "user_id": str(msg.from_user.id),
        "first_name": msg.from_user.first_name,
        "last_name": msg.from_user.last_name,
        "assistant_name": msg.text
    }
    await msg.answer("✅ Assistant's name saved.")
    await state.clear()
    await call_multi_agent_system(state=state_, modality="authorization")


@router.message(F.text, ConfigStates.weather_key)
async def save_weather_key(msg: Message, state: FSMContext):
    state_ = {
        "user_id": str(msg.from_user.id),
        "first_name": msg.from_user.first_name,
        "last_name": msg.from_user.last_name,
        "openweathermap_api_key": msg.text
    }
    await msg.answer("✅ OpenWeatherMap API key saved.")
    await state.clear()
    await call_multi_agent_system(state=state_, modality="authorization")


@router.message(F.text, ConfigStates.github_token)
async def save_github_token(msg: Message, state: FSMContext):
    state_ = {
        "user_id": str(msg.from_user.id),
        "first_name": msg.from_user.first_name,
        "last_name": msg.from_user.last_name,
        "github_token": msg.text
    }
    await msg.answer("✅ GitHub token saved.")
    await state.clear()
    await call_multi_agent_system(state=state_, modality="authorization")


@router.message(F.text, ConfigStates.tavily_key)
async def save_tavily_key(msg: Message, state: FSMContext):
    state_ = {
        "user_id": str(msg.from_user.id),
        "first_name": msg.from_user.first_name,
        "last_name": msg.from_user.last_name,
        "tavily_api_key": msg.text
    }
    await msg.answer("✅ Tavily API key saved.")
    await state.clear()
    await call_multi_agent_system(state=state_, modality="authorization")

