from datetime import datetime
from typing import Any, Dict, List
from src.database.mongodb.operations.decorator import mongodb_connect
from environment.config import config_uri

@mongodb_connect(config_uri(section='mongodb', filename='./environment/database.ini'))
def insert_one_document(db_name: str, collection_name: str, data: Dict[Any, Any], **kwargs) -> None:
    """
    Import data into MongoDB collection.

    Args:
        db_name (str): The name of the database.
        collection_name (str): The name of the collection.
        data (Dict[Any, Any]): The data to be imported.
        **kwargs: Additional keyword arguments.

    Keyword Args:
        db: The MongoDB database object.
        execution_timestamp: The execution timestamp.

    Returns:
        None
    """
    db = kwargs.get('db')
    execution_timestamp = kwargs.get('execution_timestamp')
    if db is not None and execution_timestamp is not None:
        collection = db[collection_name]
        data['_id'] = execution_timestamp
        collection.insert_one(data)

@mongodb_connect(config_uri(section='mongodb', filename='./environment/database.ini'))
def export_whole_collection(db_name: str, collection_name: str, **kwargs) -> List[Dict[Any, Any]]:
    """
    Export all data from a MongoDB collection.

    Args:
        db_name (str): The name of the database.
        collection_name (str): The name of the collection.
        **kwargs: Additional keyword arguments.

    Keyword Args:
        db: The MongoDB database object.
        execution_timestamp: The execution timestamp.

    Returns:
        List[Dict[Any, Any]]: The exported data.
    """
    db = kwargs.get('db')
    if db is not None:
        collection = db[collection_name]
        return list(collection.find())