from functools import wraps
from qdrant_client import QdrantClient

def qdrantdb_connect(config):
    def qdrantdb_connect_decorator(func):
        @wraps(func)
        def wrapper(collection_name, *args, **kwargs):
            try:
                client = QdrantClient(**config)
                kwargs['client'] = client
                # Execute the decorated function
                result = func(collection_name, *args, **kwargs)
            finally:
                # Close the client
                client.close()
            return result
        return wrapper
    return qdrantdb_connect_decorator