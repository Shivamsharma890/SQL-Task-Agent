# 🤖 AI SQL Task Agent

An AI-powered task management application that allows users to manage tasks using natural language. The application uses a LangChain-powered SQL agent with a Groq LLM to interact with a SQLite database and perform task-related CRUD operations.

Instead of writing SQL queries manually, users can simply give instructions such as:

> "Create a task to learn LangChain."

The AI agent understands the request, uses the appropriate SQL tools, interacts with the database, and returns a human-readable response.

---

## 🚀 Features

- 🤖 Natural-language task management
- 🔄 Create, Read, Update, and Delete (CRUD) operations
- 🧠 LLM-powered SQL agent using LangChain
- ⚡ Groq LLM integration for fast responses
- 🗄️ SQLite database for persistent task storage
- 🛠️ SQLDatabase Toolkit for database interaction
- 📋 Structured task management
- 💬 Conversational interaction through Streamlit
- 🔐 Environment-variable based API key management
- 📝 Custom system prompt for controlled agent behavior

---

## 🏗️ Architecture

```text
                    User
                      │
                      ▼
              Streamlit Interface
                      │
                      ▼
                LangChain Agent
                      │
                      ▼
                  Groq LLM
                      │
                      ▼
              SQL Database Tools
                      │
                      ▼
                SQLite Database
                      │
                      ▼
                  tasks Table

---

#### 🛜for Local Connection -
```text
Backend -
env\Scripts\activate (for environment activate command)
cd 'folder'
python 'python file name'

 ---

Frontend -
streamlit run 'python file name'
