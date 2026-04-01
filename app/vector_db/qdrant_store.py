from qdrant_client import QdrantClient
from qdrant_client.http import models as qdrant_models
from app.core.config import settings
import os

os.makedirs(settings.QDRANT_PATH, exist_ok=True)
qdrant_client = QdrantClient(path=settings.QDRANT_PATH)

try:
    qdrant_client.get_collection(collection_name=settings.QDRANT_COLLECTION)
except Exception:
    qdrant_client.create_collection(
        collection_name=settings.QDRANT_COLLECTION,
        vectors_config=qdrant_models.VectorParams(
            size=384,  # Default for all-MiniLM-L6-v2
            distance=qdrant_models.Distance.COSINE
        ),
    )
