import os
from dotenv import dotenv_values
import csv
import datetime
from datetime import datetime
import openai
import langchain
import langchain_openai

#from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
#from langchain_community.embeddings import OpenAIEmbeddings
#from langchain_openai import OpenAIEmbeddings

import vectorDB_stuff


# Setup OPEN AI
env_vars = dotenv_values('.env')
openai.api_key = env_vars['OPENAI_API_KEY']  # get the variable from env file
os.environ['OPENAI_API_KEY'] = env_vars['OPENAI_API_KEY']
os.environ['OPENAI_ORGANIZATION'] = env_vars['OPENAI_ORGANIZATION']



'''
# getting the models
import requests
# API endpoint for listing models
url = "https://api.openai.com/v1/models"

# Headers including authorization
headers = {
    "Authorization": f"Bearer {openai.api_key}"
}

# Make the request
response = requests.get(url, headers=headers)

# Check response status and print the list of models
if response.status_code == 200:
    models = response.json().get("data", [])
    for model in models:
        print(model["id"])
else:
    print(f"Failed to retrieve models: {response.status_code}")
    print(response.json())

# Core GPT-4 Models
gpt-4-turbo                    # A cost-effective version of GPT-4, offering up to 8,192 tokens, known for faster response times and good quality.
gpt-4-turbo-2024-04-09         # Dated version of GPT-4-turbo, representing the model as it was on April 9, 2024, for backward compatibility.

# GPT-3.5 Models
gpt-3.5-turbo                  # The standard GPT-3.5-turbo model, with up to 4,096 tokens; popular for general-purpose use due to its balance of speed and cost.
gpt-3.5-turbo-instruct         # A variant of GPT-3.5-turbo that is better fine-tuned for following instructional prompts.
gpt-3.5-turbo-0125             # Dated version of GPT-3.5-turbo from January 25, 2024; maintains compatibility with that release.
gpt-3.5-turbo-16k              # An extended context version of GPT-3.5-turbo, with up to 16,384 tokens for handling longer inputs.
gpt-3.5-turbo-1106             # Another dated variant of GPT-3.5-turbo as of November 6, 2024, providing compatibility for workflows using that release.

# GPT-4o Models (Optimized Versions)
gpt-4o-mini                    # A smaller, optimized variant of GPT-4 aimed at quicker responses, possibly with reduced capacity or accuracy.
gpt-4o                         # An optimized GPT-4 model focusing on cost and speed while maintaining core capabilities, useful for high-demand tasks.
gpt-4o-2024-05-13              # Version of GPT-4o from May 13, 2024; used for compatibility with applications requiring that release.
gpt-4o-2024-08-06              # Version of GPT-4o from August 6, 2024, used to retain the state and behavior of the model from that date.
gpt-4o-realtime-preview        # A preview version of GPT-4o optimized for real-time responses, likely experimental with very fast processing.
gpt-4o-realtime-preview-2024-10-01 # Dated variant of GPT-4o-realtime preview, reflecting the model state as of October 1, 2024.
chatgpt-4o-latest              # The most current GPT-4o model provided through ChatGPT, always reflecting the latest updates.

# GPT-4 Preview Models
gpt-4-1106-preview             # A preview version of GPT-4 released on November 6, 2024, possibly containing new or experimental features.
gpt-4-0613                     # Dated preview model of GPT-4 as of June 13, 2024, preserved for backward compatibility.
gpt-4-turbo-preview            # An early preview of GPT-4-turbo, providing a faster, optimized GPT-4 experience.
gpt-4-0125-preview             # Preview of GPT-4 from January 25, 2024, intended for workflows needing that specific release state.
gpt-4                          # The standard GPT-4 model, offering a maximum of 8,192 tokens; highly accurate but slower than the turbo version.

# Specialized Models
dall-e-3                       # The third-generation DALL-E model, focused on generating images from textual descriptions, including inpainting capabilities.
text-embedding-ada-002         # Model designed for creating text embeddings, commonly used in search, clustering, or classification tasks.
gpt-4o-audio-preview           # A preview of GPT-4 optimized for audio tasks, such as transcriptions or possibly audio-based Q&A.
gpt-4o-audio-preview-2024-10-01 # Dated variant of GPT-4o audio preview as of October 1, 2024, maintaining compatibility for specific workflows.

# Text Embedding Models
text-embedding-3-small         # A lightweight text embedding model, likely used for less complex embedding tasks where speed is prioritized over depth.
text-embedding-3-large         # A more powerful, larger embedding model designed for deeper, more nuanced text embedding requirements.

# Instruction-Tuned Models
gpt-3.5-turbo-instruct-0914    # Instruction-tuned variant of GPT-3.5-turbo, dated to September 14, 2024; optimized to better follow detailed instructions.

'''

# Setting the LLM
default_llm = {'model':"gpt-4o-mini", 'prices':{'completion': 0.6/1000000,'prompt':0.15/1000000}} #05/11/2024 prices
large_llm = {'model':"gpt-4o", 'prices':{'completion': 10/1000000,'prompt':2.5/1000000}}  #05/11/2024 prices
default_llm_name = default_llm['model']
large_llm_name = large_llm['model']
default_llm_prices = default_llm['prices']
large_llm_prices = large_llm['prices']

# Setting parameters
temperature = 0
verbose = False
max_tokens = 1000
messages = []
context = 'Nenhum contexto oferecido.' # needs to be adjusted accordingly
'''
messages=[
        {
            "role": "user",
            "content": "When is the USA independence day?",
        },
    ],
'''

def openai_get_completion(prompt, model=default_llm_name, temperature=0, verbose=False, max_tokens=500):
    messages = [{"role": "user", "content": prompt}]

    completion = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )                         #  response:        number of completion tokens:        number of prompt tokens:                       
    return completion.choices[0].message.content, completion.usage.completion_tokens, completion.usage.prompt_tokens
# Example usage:
#print(openai_get_completion('how many planets are there in the solar system?'))
# response to this question with the parameters set above:
'''
(
    """There are eight recognized planets in the solar system. They are, in order from the Sun:\n\n1. Mercury\n2. Venus\n3. \
    Earth\n4. Mars\n5. Jupiter\n6. Saturn\n7. Uranus\n8. Neptune\n\nAdditionally, there are dwarf planets, such as Pluto, \
    which was reclassified from a planet to a dwarf planet in 2006 by the International Astronomical Union.
    """, 
    86,   # these are the completion tokens
    17    # these are the prompt tokens
)
# Completion structure if you want all possible responses:
ChatCompletion(
    id='chatcmpl-APxdLj.......ZMUbU', 
    choices=[
        Choice(
            finish_reason='stop', 
            index=0, 
            logprobs=None, 
            message=ChatCompletionMessage(
                content=  """As of now, there are eight recognized planets in our solar system. \
                    They are, in order from the Sun:\n\n1. Mercury\n2. Venus\n3. Earth\n4.\
                    Mars\n5. Jupiter\n6. Saturn\n7. Uranus\n8. Neptune\n\nPluto was previously \
                    classified as the ninth planet but was reclassified as a "dwarf planet" by the \
                    International Astronomical Union in 2006.
                """,
                refusal=None, 
                role='assistant', 
                audio=None, 
                function_call=None, 
                tool_calls=None
            )
        )
    ], 
    created=1730750795, 
    model='gpt-4o-mini-2024-07-18', 
    object='chat.completion', 
    service_tier=None, 
    system_fingerprint='fp_...124f1', 
    usage=CompletionUsage
        (
            completion_tokens=88,
            prompt_tokens=17, 
            total_tokens=105, 
            completion_tokens_details=CompletionTokensDetails
                (
                    audio_tokens=None, 
                    reasoning_tokens=0
                ), 
            prompt_tokens_details=PromptTokensDetails
                (
                    audio_tokens=None, 
                    cached_tokens=0
                )   
        )
    )
'''


def openai_get_completion_from_messages(messages,
                                 model=large_llm_name,
                                 temperature=temperature,
                                 verbose=verbose,
                                 max_tokens=max_tokens):
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return [{'resposta': response.choices[0].message.content}, {'tokens': response.usage}]
'''Example complete response:
[{
    'resposta': 'The capital of France is Paris.'
    }, 
    {
        'tokens': CompletionUsage(
            completion_tokens=7, 
            prompt_tokens=14, 
            total_tokens=21, 
            completion_tokens_details=CompletionTokensDetails(
                audio_tokens=None, 
                reasoning_tokens=0
            ), 
            prompt_tokens_details=PromptTokensDetails(
                audio_tokens=None, 
                cached_tokens=0
            )
        )
    }
]
'''
# Example usage:
#print(openai_get_completion_from_messages(messages=[{"role": "user", "content": "What is the capital of France?"}]))


def openai_get_completion_with_context  (question='',
                                        system_message_content=f"You are an assistant.",
                                        user_prompt_template="You will receive a question. Use the following context to answer:\n",
                                        messages=None,
                                        model=large_llm_name,
                                        temperature=0,
                                        verbose=verbose,
                                        max_tokens=max_tokens,                                        
                                        context=context
                                        ):

    if messages is None:
        messages = []
    local_messages = [{'role': 'system', 'content': system_message_content}]
    local_messages.extend(messages)
    user_message = f"{user_prompt_template}\nContext:\n{context}\nQuestion:\n'{question}'"
    local_messages.append({'role':'user', 'content': user_message})
    response = openai_get_completion_from_messages(local_messages) # devolves [response[0],tokens[1]]
    return response
# Example usage:
'''
question = "Qual o nome da empresa?"
context = vectorDB_stuff.get_context(question)
completion = openai_get_completion_with_context(question=question,messages=messages, context=context)
print(f"Esse é o tipo da resposta: {type(completion)}")  # é uma lista
print(f"Resposta: \n{completion[0]['resposta']}")
print(f"Quant tokens da resposta: {completion[1]['tokens'].completion_tokens}\nQuant tokens do propmpt: {completion[1]['tokens'].prompt_tokens}\nQuant tokens total: {completion[1]['tokens'].total_tokens} ")
#print(context)
'''
# The example above returns the following completion:
'''
    [
        {
            'resposta': 'A empresa mencionada no contexto é chamada de "Acesso".'
        }, 
        {
            'tokens': CompletionUsage(
                completion_tokens=13, 
                prompt_tokens=569, 
                total_tokens=582, 
                completion_tokens_details=CompletionTokensDetails(
                    audio_tokens=None, reasoning_tokens=0
                ), 
                prompt_tokens_details=PromptTokensDetails(
                    audio_tokens=None, 
                    cached_tokens=0
                )
            )
        }
    ]
'''
