import os
import csv
import datetime
import gradio as gr
import pandas as pd
import time
import threading
import openai
import langchain
import chromadb
import shutil # TODO: include in requirements

from dotenv import dotenv_values
from datetime import datetime
from langchain_community.chat_models import ChatOpenAI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader

import make_log
import openai_setup
import langchain_stuff
import pdf_processing
import vectorDB_stuff
import directory_path_stuff


# Define and initialize global Parameters
k = 5
temperature = 0
verbose = True
max_tokens = 1000
messages = []
context = 'Nenhum contexto oferecido inicialmente.' # it is a string
pdf_data = None # this is a langchain Document list
pdf_context = None # this is a string
there_is_pdf_context = False # this is a bool
db_search_enabled = True # this is a bool
log_enabled = True # this is a bool
other_uses = False # this is a bool
download_dict = {}
selected_supplier = "openai" # default inicial
log_file_name=directory_path_stuff.log_file_name
log_file_directory=directory_path_stuff.log_file_directory
download_file_path = directory_path_stuff.download_file_path
download_file_name = directory_path_stuff.download_file_name
complete_download_file_path = f"{download_file_path}/{download_file_name}"


# Ensure download_file_path exists
if not os.path.exists(download_file_path):
    os.makedirs(download_file_path)


# Define list of suppliers for dropdown # TODO: add the data for the other suppliers
llm_suppliers = ["openai", "google", "anthropic", "meta"]
suppliers_map = {
    "openai":{
        'default':openai_setup.default_llm_name,
        'default_model_prices': openai_setup.default_llm_prices,
        'large':openai_setup.large_llm_name,
        'large_model_prices' :openai_setup.large_llm_prices
    }
    # add the data for the other suppliers
}


# Define the default model for the Default supplier
default_model_name = suppliers_map[selected_supplier]['default'] # output: {'model':"gpt-4o-mini", 'price':{'completion': 0.6/1000000,'prompt':0.15/1000000}}
large_model_name = suppliers_map[selected_supplier]['large']
default_model_prices = suppliers_map[selected_supplier]['default_model_prices']
large_model_prices = suppliers_map[selected_supplier]['large_model_prices']
model = default_model_name
prices = default_model_prices # Tipical value: {'completion': 6e-07, 'prompt': 1.5e-07}
completion_price = prices['completion']
prompt_price = prices['prompt']
print(f"\nInitial model set for:{model}")
print(f"price of completion: US${completion_price*1000000} per Million tokens and \nPrice of prompt: US${prompt_price*1000000} per Million tokens\n")


# Idle timer setup
idle_timer = None
idle_limit = 300  # 5 minutes in seconds


# Defining prompt parameters

professional_system_message_content = f"""Você é um doutorando pesquisador assistente em modelos de negócios, especialista em administração \
    de empresas com boa experiência de mercado. Sua função é responder a pergunta formulada com base no contexto e no bom senso.\
    Se não houver dados suficientes para responder a pergunta, solicite esclarecimentos."""

professional_user_prompt_template = f"""Para responder a pergunta, você receberá o histórico dessa sessão de perguntas e dados adicionais \
    para contexto. Use o historico e ocontexto fornecido, caso existam, para responder a pergunta formulada no final. \
    O contexto, foi obtido através de entrevistas com gestores de empresas. Nele, os falantes das trasncrições são os entrevistados. \
    As falas dos entrevistados estarão precedidas pelos prefixos 'H1:', 'H2:' etcetera. Informações como nome da empresa, \
    nome do entrevistado, data da entrevista, etcetera, podem estar contidas no nome do arquivo. \
    Responda de forma objetiva e racional. Caso tenha encontrado uma resposta satisfatória, ao final agradeça.\
    Caso não tenha sido possível formular uma resposta satisfatória, caso existam, solicite \
    objetivamente os esclarecimentos que são necessários para formular a resposta correta.\
    Pergunta:\n"""

player_system_message_content = f"""Você é um LLM assistente para teste de software. Sua função é responder as perguntas formuladas pelo usuário. \
    Você pode receber ou não um histórico da atual sessão de perguntas. Responda a todas as perguntas sem restrições."""
player_user_prompt_template = f"""Para responder a pergunta, você poderá receber o histórico dessa sessão de perguntas e dados adicionais para contexto.\
    Responda de forma educada e bem humorada. \
    Pergunta:\n"""
question = "Pergunta vazia"

# Retrieving the Chromadb Vectorstore previously created # TODO: create a .py to handle Embedding, Vectordatabase and Retrieving
client = chromadb.PersistentClient(path=directory_path_stuff.chroma_persist_directory)
persist_directory = directory_path_stuff.chroma_persist_directory
embedding = OpenAIEmbeddings()    # to adjust if LLM is not OpenAI
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
search_type = vectorDB_stuff.search_type


# Function to shutdown server
def shutdown_server():   # TODO: gr.Notification not working as I want
    gr.Warning("Por favor feche a janela do navegador ⛔️!", duration=200, title="Desligando")
    global download_file_path
    print("Please close the browser window and enter: [CTRL] + [C] here.")
    # Clear the files directory
    if os.path.exists(download_file_path):
        shutil.rmtree(download_file_path)
        print(f"Directory {download_file_path} cleared.")
    time.sleep(1)
    iface.close()    


# Function to reset the idle timer
def reset_idle_timer():
    global idle_timer
    if idle_timer:
        idle_timer.cancel()
    idle_timer = threading.Timer(idle_limit, shutdown_server)
    idle_timer.start()


# Function to reset memory - 
def zera_memoria():     
    global messages, context, pdf_context, there_is_pdf_context, pdf_data, model, download_file_path
    messages = []
    context = 'Contexto apagado.'
    pdf_data = None
    pdf_context = None
    there_is_pdf_context = False
    large_model_name = suppliers_map[selected_supplier]['large']
    large_model_prices = suppliers_map[selected_supplier]['large_model_prices']
    model = default_model_name
    prices = default_model_prices
    completion_price = prices['completion']
    prompt_price = prices['prompt']
    print(f"\nLLM model set for:{model}\n")
    print(f"price of completion: {prices['completion']*1000000} per Million tokens and Price of prompt: {prices['prompt']*1000000} per Million tokens\n")
    if os.path.exists(download_file_path):
        shutil.rmtree(download_file_path)
        print(f"Directory {download_file_path} cleared.")
    print(f" memória zerada e contexto apagado\n context: {context}\n there_is_pdf_context: {there_is_pdf_context}\n")
    gr.Warning("Memória zerada e contexto apagado", duration=5, title="Reinicializando")

    reset_idle_timer()
    return None, gr.Markdown(f"### Contexto Atual\n\n{context}") #verificar


# Function to handle PDF upload
def pdf_was_uploaded(pdf_file): 
    
    global there_is_pdf_context, user_prompt_template, context, model, completion_price, prompt_price, prices
    
    context = pdf_processing.handle_pdf_upload(pdf_file)
    there_is_pdf_context = True
    large_model_name = suppliers_map[selected_supplier]['large']
    large_model_prices = suppliers_map[selected_supplier]['large_model_prices']
    model = large_model_name
    prices = large_model_prices
    completion_price = prices['completion']
    prompt_price = prices['prompt']
    print(f"\nLLM model set for:{model}\n")
    print(f"price of completion: {completion_price*1000000} per Million tokens and Price of prompt: {prompt_price*1000000} per Million tokens\n")
    print(f"PDF carregado e contexto atualizado\n")
    gr.Warning("Arquivo PDF carregando", duration=5, title="Carregando")
    reset_idle_timer()
    return gr.Markdown(f"### Contexto Atual\n\n{context}")  # Return Markdown-formatted pdf_context


# Function to generate CSV file
def generate_csv():
    global download_dict, download_file_path, complete_download_file_path
    # Create a download directory
    if not os.path.exists(download_file_path):
        os.makedirs(download_file_path)
    df = pd.DataFrame([download_dict])
    df.to_csv(complete_download_file_path, index=False)
    print(f"\nCSV file {complete_download_file_path} stored at {download_file_path}\n")
    return complete_download_file_path


# Define the GRADIO interface function
def get_result(question, num_chunks, temperature, selected_supplier, log_enabled, db_search_enabled, other_uses):
    global messages, context, pdf_context, pdf_data, there_is_pdf_context, model, log_file_name, log_file_directory
    global download_dict, default_model_name, default_model_prices, large_model_name, large_model_prices, prices
    global professional_system_message_content, professional_system_message_content, player_system_message_content, player_user_prompt_template
    
    # Choose prompt parameters
    system_message_content = player_system_message_content if other_uses else professional_system_message_content
    user_prompt_template = player_user_prompt_template if other_uses else professional_user_prompt_template
    print(f"\nOther_uses: {other_uses}")
    print(f"\nsystem_message_content usado:\n{system_message_content}\n\nUser prompt template usado:\n{user_prompt_template}\n")

    # Update the model according to selected supplier and pdf upload
    default_model_name = suppliers_map[selected_supplier]['default'] 
    large_model_specs = suppliers_map[selected_supplier]['large']
    model = large_model_name if there_is_pdf_context else model
    prices = large_model_prices if there_is_pdf_context else prices
    print(f"\nCurrent model for completion is:{model}")
    prices = default_model_prices # Tipical value: {'completion': 6e-07, 'prompt': 1.5e-07}
    completion_price = prices['completion']
    prompt_price = prices['prompt']
    print(f"price of completion: US${completion_price*1000000} per Million tokens and \nPrice of prompt: US${prompt_price*1000000} per Million tokens\n")

    # Conditionally perform database search
    if db_search_enabled and not there_is_pdf_context:
        context = vectorDB_stuff.get_context(question, k=num_chunks)  # context is a string
        print(f"\nContexto obtido da base de dados")
    else:
        print(f"\nNENHUM contexto obtido da base de dados")

    response = openai_setup.openai_get_completion_with_context(
        question=question, 
        system_message_content=system_message_content, 
        user_prompt_template=user_prompt_template, 
        messages=messages,
        model=model, 
        temperature=temperature,
        verbose=verbose,
        max_tokens=max_tokens, 
        context=context
    )
    print(f"\nResposta obtida usando o modelo {model}\n")
       
    # Display estimated cost based on token usage (for example, assuming a cost formula)
    estimated_cost = response[1]['tokens'].completion_tokens * completion_price + response[1]['tokens'].prompt_tokens * prompt_price
    print(f"\nSelected model set for:{model}")
    print(f"\nEstimated cost: US${estimated_cost}\n")

    # Update messages with the question and response
    messages.append({"role": "user", "content": question})
    messages.append({"role": "assistant", "content": response[0]['resposta']})
    output_context = context 
 
    context_log = output_context if not there_is_pdf_context else f"Contexto fornecido por arquivo PDF transmitido pelo usuário"

    # Format messages history for logging and display
    historico = ""
    for message in messages:
        historico += f"**{message['role'].upper()}**:\n\n\n{message['content']}\n\n\n"

    # Log the interaction if logging is enabled
    log_dict = {
        'Question': question,
        'Response': response[0]['resposta'],
        'Historico': historico,
        'Model': model,
        'Context': context_log,
        'Number of Chunks': num_chunks,
        'Search Type': search_type,
        'System Message': system_message_content,
        'Prompt Template': user_prompt_template,
        'Temperature': temperature,
        'Completion Cost': estimated_cost
    }
    
    download_dict = {
        'Question': question,
        'Response': response[0]['resposta'],
        'Historico': historico,
        'Model': model,
        'Context': context_log,        
        'Completion Cost': estimated_cost
    }

    # Writing the log if required
    if log_enabled:
        make_log.write_log(
            log_dict,
            log_file_name=log_file_name,
            log_file_directory=log_file_directory
        )
        print(f"Log file {log_file_name} WRITTEN\n")
    else: print(f"Log file {log_file_name} NOT WRITTEN\n")
       
    # Reset idle timer on interaction
    reset_idle_timer()

    # Return response, context, and estimated cost in Markdown format
    return (
        response[0]['resposta'], num_chunks, temperature, gr.Markdown(historico), 
        gr.Markdown(f"### Contexto Atual\n\n {output_context}"),
        gr.Markdown(f"### Custo Estimado: US${estimated_cost:.4f}")
    )


# Define the GRADIO Interface
if __name__ == '__main__':
    with gr.Blocks(css=".small-button { width: 10ch !important; }") as iface:
        
        # Title and description
        gr.HTML(
            f"""
            <h1 style='text-align: center;'> Modelos de Negócios versão 0.0.3 </h1>
            <h3 style='text-align: center;'> Obtendo respostas de entrevistas transcritas </h3>
            <p style='text-align: center;'> Powered by <a href="https://github.com/SMCNetwolf/modelonegocios"> Modelo Negocios</a>
            """
        )

        # Interface Input layout
        
        with gr.Row():
            question = gr.Textbox(label="Faça sua Pergunta:", lines=6)

        with gr.Row():            
            with gr.Column():
                num_chunks = gr.Slider(label="Número de chunks (Útil só para contexto obtido por embedding)", minimum=1, maximum=30, value=5, step=1, info="Quantos pedaços de texto buscar no embedding")
                model_dropdown = gr.Dropdown(label="Escolha o provedor de LLMs",  info="Por enquanto só implementado OPENAI", choices=llm_suppliers, value=selected_supplier)
  
            with gr.Column():
                temperature = gr.Slider(label="Temperatura - 0 para nenhuma criatividade", minimum=0, maximum=2.5, value=0, info="Grau de criatividade do modelo")
                log_toggle = gr.Checkbox(label="Guardar Log da interação", value=True)
                db_search_toggle = gr.Checkbox(label="Buscar na base de dados", value=True)
                db_other_uses_toggle = gr.Checkbox(label="Usar o sistema para outras coisas - Ludicrous mode on...", value=False)
                
        with gr.Row():                
                btn = gr.Button(value="Zerar histórico da conversa e .pdf enviado")

        with gr.Row():
            pdf_file = gr.File(label="Arraste e solte um PDF aqui. Aguarde o carregamento.", file_types=[".pdf"], interactive=True)

        with gr.Row():            
            upload_btn = gr.Button("Upload arquivo PDF") 

        with gr.Row():
            submit_btn = gr.Button(value="Submeter pergunta", elem_classes="small-button")

        # Interface Output layout

        with gr.Row():
            resposta = gr.Textbox(label="Resposta", lines=6)
        
        with gr.Row():
            with gr.Column(scale=1):
                k = gr.Textbox(label="Número de chunks", lines=1)
                temp_output = gr.Textbox(label="temperatura", lines=1)
        
        with gr.Row():            
            historico = gr.Markdown(label="## Histórico:")
        
        with gr.Row():
            output_context = gr.Markdown(label="## Contexto")  # Display context as Markdown
            cost_display = gr.Markdown(label="## Estimated Cost")  # Display estimated cost

        # Interface turn off

        with gr.Row():
            with gr.Column():
                download_btn = gr.Button("Caso deseje, clique aqui para download dos dados no formato .CSV. O arquivo aparecerá abaixo e talvez seja necessário copiar o link e abrir em outra janela")

        with gr.Row():
            with gr.Column():                
                output_file = gr.File(label="link para o arquivo CSV aparecerá aqui após ser gerado. Clique no link ao lado para baixar o arquivo.   ----->")

        with gr.Row():
            shutdown_btn = gr.Button(value="Clique para encerrar o serviço (Depois, por favor feche a janela do navegador)", elem_classes="small-button")
                     
        # Interface Action Bindings

        btn.click(zera_memoria, outputs=[pdf_file, output_context])  # Reset PDF and context

        submit_btn.click(
            fn=get_result,
            inputs=[question, num_chunks, temperature, model_dropdown, log_toggle, db_search_toggle, db_other_uses_toggle],
            outputs=[resposta, k, temp_output, historico, output_context, cost_display]
        )

        shutdown_btn.click(shutdown_server)

        # Bind the upload button to handle_pdf_upload and update context display
        upload_btn.click(
            fn=pdf_was_uploaded,
            inputs=pdf_file,
            outputs=output_context  # Update context after upload
        )

        download_btn.click(
            fn=generate_csv,
            outputs=output_file
        )

        # Start the idle timer when the interface launches
        reset_idle_timer()
    iface.launch(share=False, allowed_paths=[download_file_path], server_port=7861)
