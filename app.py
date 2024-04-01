import os
from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI, OpenAIEmbeddings
from PIL import Image

load_dotenv()

img = Image.open(r"title_image.png")
st.set_page_config(page_title="CollegeBuddy: Best College for you", page_icon=img)
st.header("Let's find you a College📄")

directory = 'data/'
files = os.listdir(directory)

for file_name in files:
    file_path = os.path.join(directory, file_name)

    if file_path.endswith('.pdf'):
        with open(file_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
    elif file_path.endswith('.txt'):
        with open(file_path, 'r') as file:
            text = file.read()

    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    chunks = text_splitter.split_text(text)

    embeddings = OpenAIEmbeddings()
    knowledge_base = FAISS.from_texts(chunks, embeddings)

    query = st.text_input("Enter your question here")

    docs = knowledge_base.similarity_search(query)

    llm = OpenAI(temperature=0.3)
    chain = load_qa_chain(llm, chain_type="stuff")
    response = chain.run(input_documents=docs, question=query)
    st.success(response)
