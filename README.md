## Quick-Start

* Check demo.ipynb file.

## Note

1. In Qdrant, it's not allowed to insert a docuement without providing vectors. Therefore, providing default vector as a placeholder when using "get_openai_chat_completion_log" function and update the vectors later.
2. Use [fastembed](https://github.com/qdrant/fastembed) as a default embedding method to automatically embed the documents.

## Project Structure

```
project_root/
|
├── environment/                     # Dedicated folder for environment configurations
│   ├── __init__.py                  # Makes environment a Python package
│   ├── .env                         # Environment variables(API keys)
│   ├── database.ini                 # Database configurations
│   └── config.py                    # Configuration parser for database.ini
|
├── src/
│   ├── llm_api/
│   │   ├── openai.py            # Module for interacting with OpenAI API
│   │   ├── mistralai.py         # Module for interacting with Mistral AI API
│   │   ├── llm_chain.py         # Use Langchain to wrap-up LLM Chain
│   │   ├── prompts.py           # Prompt Collection for LLM integrations
│   │   └── ...
|   | 
│   ├── database/
│   │   ├── qdrant/
│   │   │   ├── operations/                 # Directory for Qdrant scripts
│   │   │   │   ├── create_operations.py    # C operations in CRUD.
│   │   │   │   └── decorator.py
│   │   │   │
│   │   │   ├── models/                    # Directory for Qdrant models or schemas
│   │   │   │   └── collection_config.py   # Schema for the collections in Qdrant
│   │   │   │
│   │   │   └── ...
│   │   │ 
│   │   ├── mongodb/
│   │   │   ├── operations/                 # Directory for MongoDB scripts
│   │   │   └── ...
│   │   │
│   │   └── database_service.py            # Database service module for handling database operations
│   |
├── tests/                         # Directory for unit tests (TBD)
│   ├── test_openai_client.py
│   ├── test_mongodb_client.py
│   └── ...
|
├── demo.ipynb                     # Demo for quick-start.
│
└── requirements.txt               # File listing project dependencies
```
