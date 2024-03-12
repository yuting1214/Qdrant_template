from qdrant_client import QdrantClient
from qdrant_client import models

# Config reference: https://qdrant.tech/documentation/guides/optimize/

def create_qdrant_collection(client: QdrantClient, collection_name: str, collection_type: str = 'high_precision_low_memory') -> None:
    """
    Create a Qdrant collection using the provided QdrantClient object.
    
    Args:
        client (QdrantClient): The QdrantClient object.
        collection_name (str): The name of the collection to be created.
    """
    collection_config = {
        'high_precision_low_memory': {
            'collection_name': collection_name,
            'vectors_config': models.VectorParams(size=768, distance=models.Distance.COSINE),
            'optimizers_config': models.OptimizersConfigDiff(memmap_threshold=20000),
            'hnsw_config': models.HnswConfigDiff(on_disk=True),
        },
        'high_precision_high_speed': {
            'collection_name': collection_name,
            'vectors_config': models.VectorParams(size=768, distance=models.Distance.COSINE),
            'optimizers_config': models.OptimizersConfigDiff(memmap_threshold=20000),
            'quantization_config': models.ScalarQuantization(scalar=models.ScalarQuantizationConfig(type=models.ScalarType.INT8,always_ram=True,),)
        },
        'high_speed_low_memory': {
            'collection_name': collection_name,
            'vectors_config': models.VectorParams(size=768, distance=models.Distance.COSINE),
            'optimizers_config': models.OptimizersConfigDiff(memmap_threshold=20000),
            'quantization_config': models.ScalarQuantization(scalar=models.ScalarQuantizationConfig(type=models.ScalarType.INT8,always_ram=True,),)
        },
        'document':{
            'collection_name': collection_name,
            'on_disk_payload': False
        }
    }
    if collection_type not in collection_config:
        raise ValueError(f"Invalid collection type: {collection_type}; Valid collection types are: {', '.join(collection_config.keys())}")

    try:
        # Create the collection using the QdrantClient
        client.create_collection(**collection_config[collection_type])
        print(f"Collection '{collection_name}' created successfully.")
    except Exception as e:
        print(f"Failed to create collection '{collection_name}': {e}")

