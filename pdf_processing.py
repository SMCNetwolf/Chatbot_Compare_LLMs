import langchain
from langchain_community.document_loaders import PyPDFLoader
import gradio as gr

import langchain_stuff

# Function to process a local PDF file
def process_pdf(file_path):
    global pdf_data
    loader = PyPDFLoader(file_path)  # Directly pass the file path to PyPDFLoader
    pdf_data = loader.load()  # Extract text to pdf_data
    return pdf_data # it is a list of langchain Documents
'''
# Example usage:
pdf_data = process_pdf("./Carlos_Acesso.pdf")
print(f"\n pdf_data[0].page_content:\n {pdf_data[0].page_content}")
print(f"\n pdf_data type: {type(pdf_data)}") # it is a list of langchain Documents
print(f"\n pdf_data[0] type: {type(pdf_data[0])}") # it is a langchain Document
'''

# Function to handle PDF upload, extracting only the text content
def handle_pdf_upload(file):
    global pdf_data # this is a langchain Document list
    global pdf_context # this is a string
    global there_is_pdf_context # this is a bool
    global context # this is a string

    pdf_data = process_pdf(file)  # Process and store PDF text in a lanchain Document list
    pdf_context = langchain_stuff.extract_text_content_from_langchain_Document_List(pdf_data)  # Update context with pdf text
    context = pdf_context
    there_is_pdf_context = True

    return context #gr.Markdown(f"### Contexto Atual\n\n{context}")  # Return Markdown-formatted pdf_context
