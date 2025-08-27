#to create the vector db we need to 1. load the documents 2. split the documents into chunks 3. create embeddings 4. store the embeddings in a vector db

from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
openai_api_key = os.getenv("OPENAI_API_KEY")

chroma_path = "chroma"
data_path = "/home/alishba/MyWork/AlishbaGIT/LangGraph-RAG.py/data/pdf/"
embeddings = OpenAIEmbeddings()

def load_documents(data_path):
    loader = DirectoryLoader(data_path, glob="**/*.pdf")
    documents = loader.load()
    print("Total number of documents loaded:", len(documents))
    return documents

#split the documents into chunks
def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len, add_start_index=True)
    texts = text_splitter.split_documents(documents)
    print("Total number of document chunks:", len(texts))
    return texts

#store the embeddings in a vector db
def create_vector_db(texts):
    if not os.path.exists(chroma_path):
        os.makedirs(chroma_path)
    vectordb = Chroma.from_documents(documents=texts, embedding=embeddings, persist_directory=chroma_path)
    vectordb.persist()
    print("Vector database created and persisted at:", chroma_path)
    return vectordb


#test the function
if __name__ == "__main__":
    docs = load_documents(data_path)
    texts = split_documents(docs)
    vectordb = create_vector_db(texts)