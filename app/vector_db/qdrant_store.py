from qdrant_client import QdrantClient
from qdrant_client.http import models as qdrant_models
from app.core.config import settings
import os

# Initialize Qdrant (local storage)
qdrant_client = QdrantClient(path="./qdrant_data")


# Create collection if not exists
try:
    qdrant_client.get_collection(collection_name=settings.QDRANT_COLLECTION)
    print("Collection already exists ✅")

except Exception:
    print("Creating new collection... 🚀")

    qdrant_client.create_collection(
        collection_name=settings.QDRANT_COLLECTION,
        vectors_config=qdrant_models.VectorParams(
            size=384,  # MiniLM embedding size
            distance=qdrant_models.Distance.COSINE
        ),
    )