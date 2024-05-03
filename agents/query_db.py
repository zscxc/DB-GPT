from langchain_community.agent_toolkits import create_sql_agent
# 从URI创建SQLDatabase实例
# 这里的"../../../../../notebooks/Chinook.db"是数据库文件的相对路径
from langchain.sql_database import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_openai import ChatOpenAI
# 加载环境变量
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

from prompts.temple import DBExpert
from memory.memory_chat_message_history import MemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import os


llm = ChatOpenAI(model="gpt-4")
class QueryDBAgent:
    @classmethod
    def nlp_query_db(cls) -> RunnableWithMessageHistory:
        # 创建PostgreSQL数据库实例
        db = SQLDatabase.from_uri(os.getenv("MYSQL_URL"))

        # 创建SQL工具包实例
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        context = toolkit.get_context()
        prompt = DBExpert.chat_prompt_message()
        prompt = prompt.partial(**context)
        agent_executor = create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            agent_type="openai-tools",
            prompt=prompt,
            verbose=True)

        agent_with_chat_history = MemoryChatMessageHistory.manage_chat_history(agent_executor)

        # reply = agent_with_chat_history.invoke(
        #     {"input": user_prompt},
        #     config={"configurable": {"session_id": "nlp2sql-session"}},
        # )
        # output_only = reply['output']
        return agent_with_chat_history


if __name__ == '__main__':
    query_db = QueryDBAgent()
    output_only = query_db.nlp_query_db("把我们系统的用户信息告诉我")
    # output_only = query_db.nlp_query_db("给我插入一条用户数据")
    print("------------------------")
    print(output_only)
