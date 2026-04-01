from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models
from app.schemas import model_schemas as schemas
from app.api.deps import require_role

router = APIRouter()

@router.post("/create", response_model=schemas.Role)
def create_role(role_in: schemas.RoleCreate, db: Session = Depends(get_db), current_user: models.User = Depends(require_role(["Admin"]))):
    role = db.query(models.Role).filter(models.Role.name == role_in.name).first()
    if role:
        raise HTTPException(status_code=400, detail="Role already exists")
    db_role = models.Role(name=role_in.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

@router.post("/assign-role")
def assign_role(user_id: int, role_name: str, db: Session = Depends(get_db), current_user: models.User = Depends(require_role(["Admin"]))):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    role = db.query(models.Role).filter(models.Role.name == role_name).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
        
    if role in user.roles:
        raise HTTPException(status_code=400, detail="User already has this role")
        
    user.roles.append(role)
    db.commit()
    return {"message": f"Role {role_name} assigned to {user.username}"}

@router.get("/{id}/roles")
def get_user_roles(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(require_role(["Admin"]))):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return [role.name for role in user.roles]

@router.get("/{id}/permissions")
def get_user_permissions(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(require_role(["Admin"]))):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    perms = set()
    for role in user.roles:
        for perm in role.permissions:
            perms.add(perm.name)
    return list(perms)
