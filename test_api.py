import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# 1. Load biến môi trường từ file .env
load_dotenv()
llm = ChatOpenAI (model="gpt-4o-mini")
print(llm.invoke("Xin chào?").content)