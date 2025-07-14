# Multi-agent Telegram Assistant

**Multi-agent Telegram Assistant** is a Telegram bot powered by a **LangGraph-based multi-agent system**. It coordinates multiple agents for tasks like web search, code execution, and API access. The bot uses PostgreSQL for memory storage and integrates with LangChain tools, all within a seamless Telegram interface.

---

## 🚀 Features

- LangGraph multi-agent orchestration
- Telegram Bot interface
- PostgreSQL-backed message history
- Web search, code execution, and API integration
- Asynchronous, modular, and configurable

---

## 🛠 Configuration

Set the following variables in `database/config.py` before running the project:

```python
# database/config.py
DATABASE_URL = "postgresql+asyncpg://user:password@host:port/dbname"
TOKEN = "your-telegram-bot-token"
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

## 📖 Notes

- Make sure your PostgreSQL database is running and accessible.
- The `TOKEN` must be a valid token from BotFather.
- All required configuration is set inside `database/config.py` before building and running the Docker container.

---

## 📝 License

MIT — Feel free to use, modify, and contribute!
