from typing import List, Dict, Any, Optional
import asyncio
from environment.config import config
from src.database.qdrant.operations.decorator import qdrantdb_connect
from src.database.utlis import generate_uuids
from qdrant_client.http import models
from qdrant_openapi_client.models import CollectionDescription

# |--------------------------------------------------------------------------|
# |                         CREATE COLLECTIONS                               |
# |--------------------------------------------------------------------------|
@qdrantdb_connect(config(section='qdrant_public', filename='./environment/database.ini'))
def create_qdrant_collection(collection_name: str,
                             collection_type: str = 'high_precision_low_memory',
                             dimensions: int = 768,
                             **kwargs) -> None:
    """
    Create a Qdrant collection using the provided QdrantClient object.
    
    Args:
        collection_name (str): The name of the collection to be created.
        collection_type (str): The type of collection to be created. Default is 'high_precision_low_memory'.
        dimensions (int): The number of dimensions of the vectors. Default is 768.
    """
    collection_config = {
        'high_precision_low_memory': {
            'collection_name': collection_name,
            'vectors_config': models.VectorParams(size=dimensions, distance=models.Distance.COSINE),
            'optimizers_config': models.OptimizersConfigDiff(memmap_threshold=20000),
            'hnsw_config': models.HnswConfigDiff(on_disk=True),
        },
        'high_precision_high_speed': {
            'collection_name': collection_name,
            'vectors_config': models.VectorParams(size=dimensions, distance=models.Distance.COSINE),
            'optimizers_config': models.OptimizersConfigDiff(memmap_threshold=20000),
            'quantization_config': models.ScalarQuantization(scalar=models.ScalarQuantizationConfig(type=models.ScalarType.INT8,always_ram=True,),)
        },
        'high_speed_low_memory': {
            'collection_name': collection_name,
            'vectors_config': models.VectorParams(size=dimensions, distance=models.Distance.COSINE),
            'optimizers_config': models.OptimizersConfigDiff(memmap_threshold=20000),
            'quantization_config': models.ScalarQuantization(scalar=models.ScalarQuantizationConfig(type=models.ScalarType.INT8,always_ram=True,),)
        },
    }
    if collection_type not in collection_config:
        raise ValueError(f"Invalid collection type: {collection_type}; Valid collection types are: {', '.join(collection_config.keys())}")

    try:
        client = kwargs.get('client')
        client.create_collection(**collection_config[collection_type])
        print(f"Collection '{collection_name}' created successfully.")
    except Exception as e:
        print(f"Failed to create collection '{collection_name}': {e}")


# |--------------------------------------------------------------------------|
# |                         INSERT DOCUMENTS                                 |
# |--------------------------------------------------------------------------|

@qdrantdb_connect(config(section='qdrant_public', filename='./environment/database.ini'))
def insert_one_document(collection_name: str,
                        ids: Optional[str],
                        vectors: List[float],
                        payloads:Optional[Dict[str, Any]],
                        **kwargs) -> None:
    # Check if collection exists
    client = kwargs.get('client')
    target_collection = CollectionDescription(name=collection_name)
    current_collections = client.get_collections().collections
    if target_collection not in current_collections:
        raise ValueError(f"Collection '{collection_name}' does not exist.")
    # Create a dictionary to hold the data
    data_dict = {}
    if ids is None:
        ids = generate_uuids(1)[0]
    data_dict['id'] = ids
    if vectors is not None:
        data_dict['vector'] = vectors
    if payloads is not None:
        data_dict['payload'] = payloads
    
    # Insert the document into the collection
    client.upsert(
        collection_name=collection_name,
        points=[models.PointStruct(**data_dict)]
    )

@qdrantdb_connect(config(section='qdrant_public', filename='./environment/database.ini'))
async def insert_one_document_async(collection_name: str,
                        ids: Optional[str],
                        vectors: List[float],
                        payloads:Optional[Dict[str, Any]],
                        **kwargs) -> None:
    # Check if collection exists
    client = kwargs.get('client')
    target_collection = CollectionDescription(name=collection_name)
    current_collections = client.get_collections().collections
    if target_collection not in current_collections:
        raise ValueError(f"Collection '{collection_name}' does not exist.")
    # Create a dictionary to hold the data
    data_dict = {}
    if ids is None:
        ids = generate_uuids(1)[0]
    data_dict['id'] = ids
    if vectors is not None:
        data_dict['vector'] = vectors
    if payloads is not None:
        data_dict['payload'] = payloads
    
    # Insert the document into the collection
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, client.upsert, collection_name, [models.PointStruct(**data_dict)])

@qdrantdb_connect(config(section='qdrant_public', filename='./environment/database.ini'))
def insert_documents(collection_name: str,
                     ids: Optional[List[str]],
                     vectors: List[List[float]],
                     payloads: Optional[List[Dict[str, Any]]],
                     **kwargs) -> None:
    # Check if collection exists
    client = kwargs.get('client')
    target_collection = CollectionDescription(name=collection_name)
    current_collections = client.get_collections().collections
    if target_collection not in current_collections:
        raise ValueError(f"Collection '{collection_name}' does not exist.")
    # Create a dictionary to hold the data
    data_dict = {}
    if len(vectors) != len(payloads):
        raise ValueError('The number of vectors and payloads should be the same')
    if ids is None:
        ids = generate_uuids(len(vectors))
    data_dict['id'] = ids
    if vectors is not None:
        data_dict['vector'] = vectors
    if payloads is not None:
        data_dict['payload'] = payloads
    
    # Insert the documents into the collection
    client.upsert(
        collection_name=collection_name,
        points=[models.Batch(**data_dict)]
    )

# |--------------------------------------------------------------------------|
# |                         INSERT AND EMBED DOCUMENTS                       |
# |--------------------------------------------------------------------------|
@qdrantdb_connect(config(section='qdrant_public', filename='./environment/database.ini'))
def insert_and_embed_documents(collection_name: str,
                                  ids: Optional[List[str]],
                                  docs: List[str],
                                  metadatas:Optional[List[Dict[str, Any]]],
                                  **kwargs) -> None:
    # Check if collection exists
    client = kwargs.get('client')

    # If you want to change the model:
    # client.set_model("sentence-transformers/all-MiniLM-L6-v2")
    # List of supported models: https://qdrant.github.io/fastembed/examples/Supported_Models

    # Prepare the documents
    if ids is None:
        ids = generate_uuids(len(docs))
    
    # Insert the documents into the collection with embeddings
    client.add(
        collection_name=collection_name,
        documents=docs,
        metadata=metadatas,
        ids=ids
    )