import os
from typing import Dict, List
import asyncio
from tqdm.asyncio import tqdm_asyncio
import time
from dotenv import load_dotenv
import logging
import openai
from openai import OpenAI, AsyncOpenAI
from src.database.qdrant.operations.create_operations import insert_one_document, insert_and_embed_documents

def get_openai_chat_completion(messages: List[Dict[str, str]],
                               model: str = "gpt-3.5-turbo",
                               temperature: float = 0,
                               max_tokens: int = 500) -> str:
    _ = load_dotenv('./environment/.env')
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        content = response.choices[0].message.content

        return content

    finally:
        # Close the client connection
        client.close()

def get_openai_chat_completion_log(collection_name: str,
                                   messages: List[Dict[str, str]],
                                   model: str = "gpt-3.5-turbo",
                                   temperature: float = 0,
                                   max_tokens: int = 500) -> str:
    _ = load_dotenv('./environment/.env')
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        content = response.choices[0].message.content
        # Log the response
        id_ = None
        vector = [i for i in range(768)]
        payload = {'messages': messages, 'content': content}
        insert_one_document(collection_name, id_, vector, payload)
        logging.info(f"Log the response to collection '{collection_name}'.")
        return content

    finally:
        # Close the client connection
        client.close()

def get_openai_chat_completion_log_and_embed(collection_name: str,
                                             messages: List[Dict[str, str]],
                                             model: str = "gpt-3.5-turbo",
                                             temperature: float = 0,
                                             max_tokens: int = 500) -> str:
    _ = load_dotenv('./environment/.env')
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        content = response.choices[0].message.content
        # Log the response
        id_ = None
        docs = [content]
        metadatas = [{'messages': messages}]
        insert_and_embed_documents(collection_name, id_, docs, metadatas)
        logging.info(f"Log the response to collection '{collection_name}'.")
        return content

    finally:
        # Close the client connection
        client.close()


# |------------------------------------------------------|
# |      Async OpenAI Chat Completion Function           |
# |------------------------------------------------------|

async def send_chat_completion_async(client,
                                     message,
                                     model,
                                     temperature,
                                     max_tokens):
    
    return await client.chat.completions.create(
        messages=[{"role": "system", "content": "You're a chatbot."},
                  {'role': "user", 'content': message}],
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )

async def get_openai_chat_completion_async(messages,
                                           model = "gpt-3.5-turbo",
                                           temperature=0,
                                           max_tokens=500,
                                           max_concurrent_requests = 5) -> None:

    async def process_message(message):
        return await send_chat_completion_async(client, message, model, temperature, max_tokens)
        
    _ = load_dotenv('./environment/.env')
    client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    tasks = []
    semaphore = asyncio.Semaphore(max_concurrent_requests)

    async def perform_task(message):
        async with semaphore:
            return await process_message(message)

    for message in messages:
        tasks.append(perform_task(message))

    return await tqdm_asyncio.gather(*tasks)

async def get_openai_chat_completion_async_sleep(messages,
                                           model = "gpt-3.5-turbo",
                                           temperature=0,
                                           max_tokens=500,
                                           max_concurrent_requests = 5) -> None:

    async def process_message(message):
        return await send_chat_completion_async(client, message, model, temperature, max_tokens)
        
    _ = load_dotenv('./environment/.env')
    client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    tasks = []
    semaphore = asyncio.Semaphore(max_concurrent_requests)

    async def perform_task(message):
        async with semaphore:
            try:
                return await process_message(message)
            except openai.RateLimitError as e:
                print("A 429 status code was received; we should back off a bit.")
                time.sleep(60)  # sleep for 60 seconds
                return await perform_task(message)  # retry the same message
            except Exception as e:
                print(f"Error processing message: {message}. Error: {e}")
                return None

    for message in messages:
        tasks.append(perform_task(message))

    return await asyncio.gather(*tasks)