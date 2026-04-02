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
    print(f"Warning: CrossEncoder failed ({e}) → using vector search fallback")
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
    print(f"Chunks created: {len(chunks)}")  # 🔍 DEBUG

    embeddings = embeddings_model.embed_documents(chunks)

    points = []
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
  
    try:
        # 🔥 FIX 1: Increase candidate pool
        res = qdrant_client.query_points(
            collection_name=settings.QDRANT_COLLECTION,
            query=query_vector,
            limit=50   # 🔥 VERY IMPORTANT (was 20)
        )

        initial_results = res.points if hasattr(res, "points") else res

    except Exception as e:
        print(f"Qdrant query failed: {e}")
        return []

    print(f"Initial results: {len(initial_results)}")  # 🔍 DEBUG

    if not initial_results:
        return []

    # 🔥 FIX 2: Cleaner filtering
    valid_hits = [
        hit for hit in initial_results
        if hit.payload and "text" in hit.payload
    ]

    print(f"Valid hits: {len(valid_hits)}")  # 🔍 DEBUG

    if not valid_hits:
        return []

    chunks = [hit.payload["text"] for hit in valid_hits]
    pairs = [[query, chunk] for chunk in chunks]

    # =========================
    # Reranking
    # =========================
    if cross_encoder is not None:
        try:
            scores = cross_encoder.predict(pairs)

            scored_results = [
                {"score": float(score), "payload": hit.payload}
                for hit, score in zip(valid_hits, scores)
            ]

        except Exception as e:
            print(f"CrossEncoder failed: {e}")
            scored_results = [
                {"score": float(hit.score), "payload": hit.payload}
                for hit in valid_hits if hasattr(hit, "score")
            ]
    else:
        scored_results = [
            {"score": float(hit.score), "payload": hit.payload}
            for hit in valid_hits if hasattr(hit, "score")
        ]

    # 🔥 FIX 3: Sort properly
    scored_results.sort(key=lambda x: x["score"], reverse=True)

    # 🔥 FIX 4: Always return top_k (max 5)
    final_results = scored_results[:top_k]

    print(f"Returned results: {len(final_results)}")  # 🔍 DEBUG

    return [res["payload"] for res in final_results]


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