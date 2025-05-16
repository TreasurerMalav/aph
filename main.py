from openai import OpenAI
#from dotenv import load_dotenv
from fpdf import FPDF
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
import streamlit as st
import uvicorn
import datetime
import os

#load_dotenv()

api_key = os.environ.get('OPENAI_API_KEY')

def generate_instructions(type, options, level, number_of_questions, answer, relevant_chunks, generate_image):
    if type == "Normal Quiz":
        if len(relevant_chunks) == 0:
            instructions = f"""You are an AI assistant who is expert in generating quiz for the given user query.

            Rules/parameters to follow while generating quiz.

            type = {type} # type of quiz
            options = {options} # number of options to give for a question.
            level = {level} # question difficulty level: easy, medium, hard.
            number_of_questions = {number_of_questions} # number of questions to generate for the quiz.
            answer = {answer} # True or False. If true provide answers, else don't provide answers.
            generate_image = {generate_image} # True or False. If true add relevant image for each question. If false, don't add relevant image.

            Example:
            user_query: Generate quiz on IPL seasons 2008 to 2025.
            arguements:
            type: Normal Quiz
            options: 2
            level: easy
            number_of_questions: 2
            answer: True
            generate_image: True

            Response:
            Question 1
            Who won the inaugural IPL season in 2008?
            <image>
            Options: A. Rajasthan Royals B. Chennai Super Kings
            Answer: A. Rajasthan Royals

            Question 2
            Who was the Orange Cap winner (most runs in a season) in IPL 2016?
            <image>
            Options: A. David Warner B. Virat Kohli
            Answer: B. Virat Kohli

            """
        
        else:
            instructions = f"""You are an AI assistant who is expert in generating quiz for the given user query from given context. If context is not relevant to user_query, please inform that I have no relevant data to generate the quiz.

            context:
            {relevant_chunks}

            Rules/parameters to follow while generating quiz.

            type = {type} # type of quiz
            options = {options} # number of options to give for a question.
            level = {level} # question difficulty level: easy, medium, hard.
            number_of_questions = {number_of_questions} # number of questions to generate for the quiz.
            answer = {answer} # True or False. If true provide answers, else don't provide answers.
            generate_image = {generate_image} # True or False. If true add relevant image for each question. If false, don't add relevant image.

            Example:
            user_query: Generate quiz on interesting facts about bollywood.
            arguements:
            type: Normal Quiz
            options: 2
            level: easy
            number_of_questions: 2
            answer: True
            generate_image: True

            Response:
            Question 1
            Which Bollywood movie was enlisted as a case study for Media Management students in Spain due to its impact on tourism?
            <image>
            Options: A. Zindagi Na Milegi Dobara B. 3 Idiots
            Answer: A. Zindagi Na Milegi Dobara

            Question 2
            Who stayed in Raj Kapoor’s garage during their struggling days in Bollywood?
            <image>
            Options: A. Shah Rukh Khan B. Anil Kapoor
            Answer: B. Anil Kapoor

            """

    return instructions

def generate_response(topic, instructions):

    client = OpenAI()

    response = client.responses.create(
        model = "gpt-4.1",
        input = topic,
        instructions = instructions
    )

    return response.output_text

def generate_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    text_content = text
    pdf.multi_cell(0, 10, txt=text_content, align='L')
    pdf_name = "quiz-" + str(datetime.now().timestamp()) + ".pdf"
    pdf.output(pdf_name)

#def main():
#    topic = input("Enter topic to generate quiz:\n")
#    instructions = generate_instructions(0, "hard", 5, True, False)
#    response = generate_response(topic, instructions)
#    print(response)
    #generate_pdf(response)



#app = FastAPI()
#
#templates = Jinja2Templates(directory="templates")

#@app.get("/")
#def home():
#    return "Hello from APH AI Quiz Generator!"

#if __name__ == "__main__":
#    main()
    #uvicorn.run("main:app", port=5000, log_level="info")

#import time

st.title("APH AI Quiz Generator")

website_link = st.sidebar.text_input("Enter website link from which you want to create quiz")
index_data = st.sidebar.button("Index Data")
quiz_type = st.sidebar.selectbox("Select type of Quiz Game", ["Normal Quiz"])
search_from_website_list = [] # add jumbled words in future
#search_from_website = st.sidebar.multiselect("Select website", search_from_website_list)
user_query = st.sidebar.text_input("Enter quiz topic to generate")
quiz_level = st.sidebar.selectbox("Select difficulty level of Quiz Game", ["Easy", "Medium", "Hard"])
number_of_questions = st.sidebar.number_input("Select number of questions", min_value=1, max_value=20, step=1)
number_of_options = st.sidebar.number_input("Select number of options", min_value=0, max_value=4, step=2)
require_answers = st.sidebar.checkbox("Require Answers?", value=True)
#generate_image = st.sidebar.checkbox("Generate Image?", value=False)
generate_from_indexed_data = st.sidebar.checkbox("Generate from Indexed Data?", value=False)
submit = st.sidebar.button("Submit")

embeddings = OpenAIEmbeddings(
model="text-embedding-3-large",
api_key=api_key
)

if index_data and website_link:
    status = st.status("Data ingestion in progress ...")
    loader = WebBaseLoader(website_link)
    loader.requests_kwargs = {'verify':False}
    docs = loader.load()
    #st.write(len(docs))
    #st.write(docs[0])
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    split_docs = text_splitter.split_documents(docs)
    #st.write(len(texts))
    #st.write(texts)

    collection_name = str(datetime.date.today())

    vector_store = QdrantVectorStore.from_documents(
        documents=[],
        url="http://localhost:6333",
        collection_name=collection_name,
        embedding=embeddings
    ) 

    vector_store.add_documents(documents=split_docs)

    status.update(label="Data Ingested successfully", state="complete", expanded=False)
    search_from_website_list = search_from_website_list.append(website_link)

if submit and generate_from_indexed_data is False:
    status = st.status("Generating Quiz ...")
    instructions = generate_instructions(quiz_type, number_of_options, quiz_level, number_of_questions, require_answers, [],generate_image=False)
    response = generate_response(user_query, instructions)
    #time.sleep(5)
    status.update(label="Quiz Generated", state="complete", expanded=False)
    st.write(response)


if submit and generate_from_indexed_data is True:
    status = st.status("Generating Quiz ...")
    retriever = QdrantVectorStore.from_existing_collection(
        url="http://localhost:6333",
        collection_name=str(datetime.date.today()),
        embedding=embeddings
    )
    relevant_chunks = retriever.similarity_search(
        query=user_query
    )
    instructions = generate_instructions(quiz_type, number_of_options, quiz_level, number_of_questions, require_answers, relevant_chunks, generate_image=False)
    response = generate_response(user_query, instructions)
    status.update(label="Quiz Generated", state="complete", expanded=False)
    st.write(response)
