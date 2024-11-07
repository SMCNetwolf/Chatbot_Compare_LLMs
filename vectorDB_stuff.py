import os
import openai
import chromadb

from dotenv import dotenv_values
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

import directory_path_stuff
import langchain_stuff


# Setup OPEN AI
env_vars = dotenv_values('.env')
openai.api_key = env_vars['OPENAI_AIBMNLAB']  # get the variable from env file
os.environ['OPENAI_API_KEY'] = env_vars['OPENAI_AIBMNLAB']
os.environ['OPENAI_ORGANIZATION'] = env_vars['OPENAI_AIBMNLAB_ORG']

chroma_persist_directory = directory_path_stuff.chroma_persist_directory

# Retrieving the Chromadb Vectorstore previously created
client = chromadb.PersistentClient(path=chroma_persist_directory)
persist_directory = chroma_persist_directory
embedding = OpenAIEmbeddings()    # to adjust if LLM is not OpenAI
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
search_type = "similarity"


def get_context(question, k=5):
    retriever = vectordb.as_retriever(search_type=search_type, search_kwargs={"k": k})
    docs = retriever.invoke(question) #it is a list of langchain Document
    global context
    
    context = ""

    context = langchain_stuff.extract_text_content_from_langchain_Document_List(docs)
   
    return context  # Return the context as a string, "Context extracted from the database"
# Example usage:
'''
question = "Qual o nome da empresa?"
#print(type(get_context(question)[0]))
print(get_context(question))
#get_context(question)
#print(type(context))
'''