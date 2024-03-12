import os
from typing import List
from tqdm import tqdm
from collections import OrderedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_mistralai.chat_models import ChatMistralAI
from src.llm_api.prompts import VOCABULARY_EXTRACTOR_PROMPT_v3
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain.output_parsers.json import SimpleJsonOutputParser
from langchain_core.runnables import RunnablePassthrough

_ = load_dotenv('./environment/.env')

def vocabulary_extractor_chain(corpora: List[str], llm_vendor: str = "openai") -> List[str]:
    """
    Extracts vocabulary from the given corpora using a language model API.

    Args:
        corpora (List[str]): A list of strings representing the corpora.
        llm_vendor (str, optional): The language model vendor to use. Defaults to "openai".

    Returns:
        List[str]: A list of extracted vocabulary.

    Raises:
        ValueError: If an invalid LLM vendor is provided.

    Example:
        corpora = ["This is the first document.", "This is the second document."]
        vocabulary = vocabulary_extractor_chain(corpora, llm_vendor="openai")
        print(vocabulary)
        # Output: ['This', 'is', 'the', 'first', 'document', 'second']
    """
    if llm_vendor == "openai":
        model = ChatOpenAI(model="gpt-3.5-turbo",
                        openai_api_key=os.getenv('OPENAI_API_KEY'),
                        temperature = 0)
    elif llm_vendor == "mistral":
        model = ChatMistralAI(model="open-mixtral-8x7b",
                        mistral_api_key=os.getenv('MISTRAL_API_KEY'),
                        temperature = 0)
    else:
        raise ValueError("Invalid LLM vendor. Please choose 'openai' or 'mistral'.")
        
    chat_template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=(VOCABULARY_EXTRACTOR_PROMPT_v3)
            ),
            HumanMessagePromptTemplate.from_template("{corpus}"),
        ]
    )
    json_parser = SimpleJsonOutputParser()
    chain = (
        {"corpus": RunnablePassthrough()} 
        | chat_template
        | model
        | json_parser
    )

    # Add tqdm for progress bar
    responses = []
    with tqdm(total=len(corpora)) as pbar:
        for response in chain.batch(corpora, config={"max_concurrency": 5}):
            responses.append(response)
            pbar.update(1)

    return responses
