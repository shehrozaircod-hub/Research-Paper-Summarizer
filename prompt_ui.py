from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import streamlit as st
import os   

load_dotenv()

model = ChatOpenAI(model ='gpt-4o', max_tokens = 2000)

st.header('Research Tool')

user_input = st.text_input('Enter your Prompt')

if st.button('Summarize'):
    result = model.invoke(user_input)
    st.write(result.content)
