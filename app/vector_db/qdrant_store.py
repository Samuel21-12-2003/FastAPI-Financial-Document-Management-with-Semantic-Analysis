from qdrant_client import QdrantClient
from qdrant_client.http import models as qdrant_models
from app.core.config import settings
import os

# Use Qdrant Cloud (NOT local path)
qdrant_client = QdrantClient(
    url=os.getenv("https://6f2e7217-a30d-4583-93a3-f2f414b442a9.eu-west-2-0.aws.cloud.qdrant.io:6333"),
    api_key=os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwic3ViamVjdCI6ImFwaS1rZXk6NzVjNzFjODItYjE2ZC00Yjg2LWI2YTctZWFhYjQzN2FhNzI3In0.4kqS6f-OPB5JhnHoq9hoYw6LPuCML8V7WaqcNlELFds"),
)

# Create collection if not exists
try:
    qdrant_client.get_collection(collection_name=settings.QDRANT_COLLECTION)
except Exception:
    qdrant_client.create_collection(
        collection_name=settings.QDRANT_COLLECTION,
        vectors_config=qdrant_models.VectorParams(
            size=384,  # for MiniLM
            distance=qdrant_models.Distance.COSINE
        ),
)