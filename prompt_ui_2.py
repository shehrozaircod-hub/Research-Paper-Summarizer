from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate, load_prompt
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

model = ChatOpenAI(model='gpt-4o', max_tokens=2000)

st.header('Research Tool')

paper_input = st.selectbox("Select Research Paper Name", ["Attention Is All You Need", 
                                                          "BERT: Pre-training of Deep Bidirectional Transformers", 
                                                          "GPT-3: Language Models are Few-Shot Learners", 
                                                          "Diffusion Models Beat GANs on Image Synthesis"])

style_input = st.selectbox("Select Summary Style", ["Beginner_Friendly",
                                                     "Technical",
                                                     "Code_Oriented",
                                                     "Mathematical"])

length_input = st.selectbox("Select Summary Length", ["Short (1-2 paragraphs)",
                                                       "Medium (3-5 paragraphs)",
                                                       "Long (detailed_explanation)"])

# Template

template = load_prompt('template.json')

#fill the placeholders
prompt = template.invoke({
    'a':paper_input,
    'b':style_input,
    'c':length_input
})


if st.button('Summarize'):
    result = model.invoke(prompt)
    st.write(result.content)