from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(
    model = 'gpt-4o'
)

chat_template = ChatPromptTemplate([
    ("system", "You are a helpful {domain} expert."),
    ("human", "Explain {topic} in simple terms.")
])

prompt = chat_template.format_messages(domain='Physics', topic='quantam entanglement')

response = model.invoke(prompt)

print(prompt)
print(response.content)