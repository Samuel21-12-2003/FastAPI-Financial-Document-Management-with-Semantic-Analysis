from app.vector_db.qdrant_store import qdrant_client

print(f"Type: {type(qdrant_client)}")
print(f"Dir: {dir(qdrant_client)}")
import qdrant_client as qc
print("Version:", getattr(qc, '__version__', 'unknown'))
