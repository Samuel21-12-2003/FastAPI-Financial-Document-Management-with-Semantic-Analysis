import os
import uuid
import shutil
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models
from app.schemas import model_schemas as schemas
from app.api.deps import get_current_active_user, require_role

router = APIRouter()

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=schemas.Document)
def upload_document(
    title: str = Form(...),
    company_name: str = Form(...),
    document_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["Admin", "Analyst"]))
):
    # Save file
    file_id = str(uuid.uuid4())
    file_ext = os.path.splitext(file.filename)[1]
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}{file_ext}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    db_document = models.Document(
        title=title,
        company_name=company_name,
        document_type=document_type,
        uploaded_by=current_user.id,
        file_path=file_path,
        is_indexed=False
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

@router.get("", response_model=List[schemas.Document])
def get_all_documents(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    docs = db.query(models.Document).offset(skip).limit(limit).all()
    return docs

@router.get("/search", response_model=List[schemas.Document])
def search_documents_by_metadata(
    title: Optional[str] = None,
    company_name: Optional[str] = None,
    document_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    query = db.query(models.Document)
    if title:
        query = query.filter(models.Document.title.ilike(f"%{title}%"))
    if company_name:
        query = query.filter(models.Document.company_name.ilike(f"%{company_name}%"))
    if document_type:
        query = query.filter(models.Document.document_type == document_type)
        
    return query.all()

@router.get("/{document_id}", response_model=schemas.Document)
def get_document(document_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    doc = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.delete("/{document_id}")
def delete_document(
    document_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(require_role(["Admin", "Analyst"]))
):
    doc = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    # Remove file
    if os.path.exists(doc.file_path):
        os.remove(doc.file_path)
        
    db.delete(doc)
    db.commit()
    return {"message": "Document deleted"}
