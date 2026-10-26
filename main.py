from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from toolcreation import get_conversion_factor, convert
from langchain_core.messages import HumanMessage
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest"                   
)

llm_with_tools = llm.bind_tools([get_conversion_factor,convert])

messages = [HumanMessage('What is the conversion factor between INR and USD, and based on that can you convert 10 inr to usd')]


ai_response = llm_with_tools.invoke(messages)

print(ai_response.tool_calls())