from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b")
db = SQLDatabase.from_uri("sqlite:///my_database.db")

db.run("""
       CREATE TABLE IF NOT EXISTS tasks (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           title TEXT NOT NULL,
           Description TEXT,
           status TEXT CHECK (status IN ('pending', 'in_progress', 'completed')) DEFAULT 'pending',
           created_at TIMESTAMP DEFAULT (datetime('now', '+5 hours', '+30 minutes'))
        );
""")


toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()


system_prompt = """
You are a task management assistant that interacts with a SQL database containing a 'tasks' table.

Your job is to help users create, read, update, and delete tasks using the available SQL database tools.

TASK RULES:
1. Limit SELECT queries to a maximum of 10 results.Always use ORDER BY created_at DESC when listing tasks so that the newest tasks appear first.
2. After every CREATE, UPDATE, or DELETE operation, confirm that the operation was successful by executing a SELECT query.
3. If the user requests a list of tasks, present the output in a clear and structured table format.

CRUD OPERATIONS:
CREATE : INSERT INTO tasks(title, description, status)
READ : SELECT * FROM tasks WHERE ... ORDER BY created_at DESC LIMIT 10
UPDATE : UPDATE tasks SET status = ? WHERE id = ? OR title = ?
DELETE : DELETE FROM tasks WHERE id = ? OR title = ?

Table schema: id, title, description, status(pending/in_progress/completed), created_at.
"""


@st.cache_resource             ### using this decorator in streamlit so that our previous memory not reload again and again..
def load_agent():
    agent = create_agent(
        model=llm,
        tools=tools,
        checkpointer=InMemorySaver(),
        system_prompt=system_prompt,
    )
    return agent


agent = load_agent()

st.subheader("📜TaskBot - an Database agent manage your Tasks")

if "history" not in st.session_state:
    st.session_state.history = []

for message in st.session_state.history:
    role = message["role"]
    content = message["content"]
    st.chat_message(role).markdown(content)

query = st.chat_input("Ask me to manage your Tasks ?")
if query:
    st.session_state.history.append({"role": "user", "content": query})
    st.chat_message("user").markdown(query)
    with st.chat_message("ai"):
        with st.spinner("processing..."):
            res = agent.invoke(
                {"messages": [{"role": "user", "content": query}]},
                {"configurable": {"thread_id": "1"}},
            )
            result = res["messages"][-1].content
            st.markdown(result)
            st.session_state.history.append({"role": "ai", "content": result})
