import uuid
from typing import List, Dict, Any

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from qdrant_client.http import models as qdrant_models
from app.vector_db.qdrant_store import qdrant_client
from app.core.config import settings

from sentence_transformers import CrossEncoder


# =========================
# Embedding Model
# =========================
embeddings_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# =========================
# Cross Encoder (Reranking)
# =========================
try:
    cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
except Exception as e:
    print(f"Warning: CrossEncoder failed to load ({e}). Falling back to vector search.")
    cross_encoder = None


# =========================
# Text Splitter
# =========================
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)


# =========================
# Index Document
# =========================
def index_document_chunks(document_id: int, text: str, metadata: Dict[str, Any]):
    chunks = text_splitter.split_text(text)
    points = []

    embeddings = embeddings_model.embed_documents(chunks)

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        point_id = str(uuid.uuid4())

        payload = {
            "document_id": document_id,
            "chunk_index": i,
            "text": chunk,
            **metadata
        }

        points.append(
            qdrant_models.PointStruct(
                id=point_id,
                vector=embedding,
                payload=payload
            )
        )

    qdrant_client.upsert(
        collection_name=settings.QDRANT_COLLECTION,
        points=points
    )


# =========================
# Delete Document
# =========================
def remove_document_vectors(document_id: int):
    qdrant_client.delete(
        collection_name=settings.QDRANT_COLLECTION,
        points_selector=qdrant_models.FilterSelector(
            filter=qdrant_models.Filter(
                must=[
                    qdrant_models.FieldCondition(
                        key="document_id",
                        match=qdrant_models.MatchValue(value=document_id)
                    )
                ]
            )
        )
    )


# =========================
# Semantic Search + Reranking
# =========================
def semantic_search_with_reranking(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    query_vector = embeddings_model.embed_query(query)

    # 🔥 FIX: Only use new Qdrant API
    try:
        res = qdrant_client.query_points(
            collection_name=settings.QDRANT_COLLECTION,
            query=query_vector,
            limit=20
        )

        # Handle response safely
        if hasattr(res, "points"):
            initial_results = res.points
        else:
            initial_results = res

    except Exception as e:
        print(f"Qdrant query failed: {e}")
        return []

    if not initial_results:
        return []

    # Extract valid chunks safely
    valid_hits = []
    chunks = []

    for hit in initial_results:
        if hit.payload and "text" in hit.payload:
            valid_hits.append(hit)
            chunks.append(hit.payload["text"])

    if not chunks:
        return []

    # Prepare for reranking
    pairs = [[query, chunk] for chunk in chunks]

    # =========================
    # Reranking using CrossEncoder
    # =========================
    if cross_encoder is not None:
        try:
            scores = cross_encoder.predict(pairs)

            scored_results = [
                {"score": float(score), "payload": hit.payload}
                for hit, score in zip(valid_hits, scores)
            ]

            scored_results.sort(key=lambda x: x["score"], reverse=True)

            return [res["payload"] for res in scored_results[:top_k]]

        except Exception as e:
            print(f"CrossEncoder failed: {e}, using vector similarity fallback")

    # =========================
    # Fallback: Vector similarity
    # =========================
    scored_results = [
        {"score": float(hit.score), "payload": hit.payload}
        for hit in valid_hits if hasattr(hit, "score")
    ]

    scored_results.sort(key=lambda x: x["score"], reverse=True)

    return [res["payload"] for res in scored_results[:top_k]]


# =========================
# Get Document Context
# =========================
def get_document_context(document_id: int) -> List[Dict[str, Any]]:
    results, _ = qdrant_client.scroll(
        collection_name=settings.QDRANT_COLLECTION,
        scroll_filter=qdrant_models.Filter(
            must=[
                qdrant_models.FieldCondition(
                    key="document_id",
                    match=qdrant_models.MatchValue(value=document_id)
                )
            ]
        ),
        limit=100
    )

    return [hit.payload for hit in results]