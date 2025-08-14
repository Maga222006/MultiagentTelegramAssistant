# Multi-agent Telegram Assistant

**MultiagentTelegramAssistant** is a Telegram bot wrapper built on top of [MultiagentPersonalAssistant](https://github.com/Maga222006/MultiagentPersonalAssistant). It provides a user-friendly Telegram interface to interact with a LangGraph-powered multi-agent system capable of handling tasks such as web search, code execution, weather queries, and more.

The core logic of the assistant—including agent coordination, tool execution, and memory—is implemented in the `MultiagentPersonalAssistant` backend. This repository simply wraps that functionality in a Telegram bot interface using **Aiogram**.

---

## 🚀 Features

- Acts as a Telegram-based interface for the multi-agent assistant  
- Sends user prompts to the backend agent system  
- Returns LLM-generated, tool-enhanced responses  

---

## 🛠 Configuration

Set the following variables in `.env` before running the project:

```.env
BOT_TOKEN = <telegram_bot_token>
BASE_URL = <multiagent_personal_assistant_server_url>
```

---

## 🐳 Running with Docker

### 1️⃣ Clone the repository:

```bash
git clone https://github.com/yourusername/MultiagentTelegramAssistant.git
cd MultiagentTelegramAssistant
```

### 2️⃣ Build the Docker image:

```bash
docker build -t multiagent-telegram-assistant .
```

### 3️⃣ Run the container:

```bash
docker run -d --name multiagent-telegram-assistant multiagent-telegram-assistant
```

---

## 📝 License

MIT — Feel free to use, modify, and contribute!
