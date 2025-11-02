from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(
    model = "gpt-5"
)

messages = [
    SystemMessage(content='You are a helpful assistant'),
    HumanMessage(content='Tell me about Langchain')
]

result = model.invoke(messages)

messages.append(AIMessage(content=result.content))

print(messages)