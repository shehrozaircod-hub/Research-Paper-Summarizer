from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
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

template = PromptTemplate(
    template = """ Please summarize the research paper titled "{a}" with the following specifications:
Explanation Style: {b}
Explanation Length: {c}
1. Mathematical Details:
-Include relevant mathematical equations if present in the paper.
-Explain the mathematical concepts using simple, intuitive code snippets where applicable.
2. Analogies:
-Use relatable analogies to simplify complex ideas.
If certain information is not available in the paper, respond with: "Insufficient information available" instead of guessing.
Ensure the summary is clear, accurate, and aligned with the provided style and length.
""",
input_variables=['a','b','c']
)

#fill the placeholders
prompt = template.invoke({
    'a':paper_input,
    'b':style_input,
    'c':length_input
})


if st.button('Summarize'):
    result = model.invoke(prompt)
    st.write(result.content)