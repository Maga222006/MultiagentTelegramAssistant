from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def get_main_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="📍 Send Location", request_location=True)],
        [KeyboardButton(text="💾 Clear Chat History",)],
        [KeyboardButton(text="🤖 Set Assistant Name", )],
        [KeyboardButton(text="🌐 Set OpenAI API Base")],
        [KeyboardButton(text="🔑 Set OpenAI API Key")],
        [KeyboardButton(text="🧠 Set Model")],
        [KeyboardButton(text="🧠 Set Spare Model")],
        [KeyboardButton(text="🎧 Set STT Model")],
        [KeyboardButton(text="☁️ Set OpenWeatherMap Key")],
        [KeyboardButton(text="💙 Set GitHub Token")],
        [KeyboardButton(text="🔍 Set Tavily API Key")]

    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Choose a config action or send location"
    )