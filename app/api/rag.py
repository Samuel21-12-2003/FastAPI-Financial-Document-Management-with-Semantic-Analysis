from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models
from app.schemas import model_schemas as schemas
from app.api.deps import require_role, get_current_active_user
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models
from app.schemas import model_schemas as schemas
from app.api.deps import require_role, get_current_active_user
from app.services import file_parser, rag_service
import os

router = APIRouter()

@router.post("/index-document")
def index_document(document_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(require_role(["Admin", "Analyst"]))):
    doc = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    if doc.is_indexed:
        return {"message": "Document is already indexed"}
        
    if not os.path.exists(doc.file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")
        
    try:
        text = file_parser.extract_text_from_file(doc.file_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse document: {e}")
        
    metadata = {
        "title": doc.title,
        "company_name": doc.company_name,
        "document_type": doc.document_type
    }
    
    rag_service.index_document_chunks(doc.id, text, metadata)
    
    doc.is_indexed = True
    db.commit()
    return {"message": f"Successfully indexed document {doc.id}"}

@router.delete("/remove-document/{id}")
def remove_document(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(require_role(["Admin", "Analyst"]))):
    doc = db.query(models.Document).filter(models.Document.id == id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    rag_service.remove_document_vectors(id)
    doc.is_indexed = False
    db.commit()
    return {"message": f"Removed vectors for document {id}"}

@router.post("/search")
def search(query_data: schemas.SearchQuery, current_user: models.User = Depends(get_current_active_user)):
    results = rag_service.semantic_search_with_reranking(query_data.query, top_k=5)
    return results

@router.get("/context/{document_id}")
def get_context(document_id: int, current_user: models.User = Depends(get_current_active_user)):
    results = rag_service.get_document_context(document_id)
    return {"document_id": document_id, "chunks": results}
app.services import file_parser, rag_service
import os

router = APIRouter()

@router.post("/index-document")
def index_document(document_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(require_role(["Admin", "Analyst"]))):
    doc = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    if doc.is_indexed:
        return {"message": "Document is already indexed"}
        
    if not os.path.exists(doc.file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")
        
    try:
        text = file_parser.extract_text_from_file(doc.file_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse document: {e}")
        
    metadata = {
        "title": doc.title,
        "company_name": doc.company_name,
        "document_type": doc.document_type
    }
    
    rag_service.index_document_chunks(doc.id, text, metadata)
    
    doc.is_indexed = True
    db.commit()
    return {"message": f"Successfully indexed document {doc.id}"}

@router.delete("/remove-document/{id}")
def remove_document(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(require_role(["Admin", "Analyst"]))):
    doc = db.query(models.Document).filter(models.Document.id == id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    rag_service.remove_document_vectors(id)
    doc.is_indexed = False
    db.commit()
    return {"message": f"Removed vectors for document {id}"}

@router.post("/search")
def search(query_data: schemas.SearchQuery, current_user: models.User = Depends(get_current_active_user)):
    results = rag_service.semantic_search_with_reranking(query_data.query, top_k=5)[:5]
    return results

@router.get("/context/{document_id}")
def get_context(document_id: int, current_user: models.User = Depends(get_current_active_user)):
    results = rag_service.get_document_context(document_id)
    return {"document_id": document_id, "chunks": results} 