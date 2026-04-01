from app.db.database import SessionLocal, Base, engine
from app.db import models
from app.core import security
import os

def create_initial_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Check if admin exists
    admin_user = db.query(models.User).filter(models.User.username == "admin").first()
    if not admin_user:
        admin_role = db.query(models.Role).filter(models.Role.name == "Admin").first()
        if not admin_role:
            admin_role = models.Role(name="Admin")
            db.add(admin_role)
            db.commit()
            db.refresh(admin_role)
            
        hashed_password = security.get_password_hash("admin")
        admin_user = models.User(
            username="admin",
            email="admin@example.com",
            hashed_password=hashed_password
        )
        admin_user.roles.append(admin_role)
        db.add(admin_user)
        db.commit()
        print("Created default admin user (username: admin, password: admin)")
    else:
        print("Admin user already exists.")
        
    db.close()

if __name__ == "__main__":
    create_initial_data()
