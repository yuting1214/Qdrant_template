from functools import wraps
from typing import Any, Dict
from pymongo import MongoClient
from datetime import datetime
from environment.config import config_uri

def mongodb_connect(config):
    def mongodb_connect_decorator(func):
        @wraps(func)
        def wrapper(db_name, collection_name, *args, **kwargs):
            # Connect to MongoDB
            with MongoClient(config) as client:
                db = client[db_name]
                execution_timestamp = datetime.now()
                # Add db and execution_timestamp to kwargs
                kwargs['db'] = db
                kwargs['execution_timestamp'] = execution_timestamp
                # Execute the decorated function
                result = func(db_name, collection_name, *args, **kwargs)
            return result
        return wrapper
    return mongodb_connect_decorator