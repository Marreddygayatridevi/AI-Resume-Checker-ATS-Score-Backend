# from fastapi import APIRouter, UploadFile, Form, File, HTTPException, Depends
# from sqlalchemy.orm import Session
# from database import SessionLocal
# from models import User
# from resume_parser import parse_resume
# from pydantic import BaseModel, EmailStr


# router = APIRouter()

# class UserRegister(BaseModel):
#     name: str
#     email: EmailStr

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # --- User Registration ---
# @router.post("/register/")
# def register_user(
#     name: str = Form(...),
#     email: str = Form(...),
#     db: Session = Depends(get_db)
# ):
#     existing_user = db.query(User).filter(User.email == email).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="User already registered.")
    
#     new_user = User(name=name, email=email)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return {"message": "User registered successfully", "user_id": new_user.id}

# # --- Resume Upload ---
# @router.post("/upload/")
# async def upload_resume(
#     email: str = Form(...),
#     role: str = Form(...),
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db)
# ):
#     if file.content_type != "application/pdf":
#         raise HTTPException(status_code=400, detail="Only PDF files allowed.")
    
#     pdf_bytes = await file.read()

    
#     if len(pdf_bytes) > 200 * 1024:
#         raise HTTPException(status_code=400, detail="PDF too large (max 200KB).")

#     user = db.query(User).filter(User.email == email).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not registered.")

#     # Parse the resume
#     parsed = parse_resume(pdf_bytes)

#     # Update user info
#     user.role = role
#     user.resume_pdf = pdf_bytes
#     user.phone = parsed.get("phone", "")
#     user.github = parsed.get("github", "")
#     user.linkedin = parsed.get("linkedin", "")
#     user.resume_text = parsed.get("resume_text", "")
    
#     db.commit()
    
#     return {"message": "Resume uploaded and parsed successfully", "user_id": user.id}
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from database import SessionLocal
from models import User
from resume_parser import parse_resume

router = APIRouter()

# --- Pydantic Schema for JSON Registration ---
class UserRegister(BaseModel):
    name: str
    email: EmailStr

# --- DB Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- User Registration (JSON) ---
@router.post("/register/")
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered.")
    
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "user_id": new_user.id}

# --- Resume Upload (multipart/form-data for file support) ---
@router.post("/upload/")
async def upload_resume(
    email: str = Form(...),
    role: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files allowed.")
    
    pdf_bytes = await file.read()

    if len(pdf_bytes) > 400 * 1024:
        raise HTTPException(status_code=400, detail="PDF too large (max 400KB).")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not registered.")

    # Parse the resume
    parsed = parse_resume(pdf_bytes)

    # Update user info
    user.role = role
    user.resume_pdf = pdf_bytes
    user.phone = parsed.get("phone", "")
    user.github = parsed.get("github", "")
    user.linkedin = parsed.get("linkedin", "")
    user.resume_text = parsed.get("resume_text", "")
    
    db.commit()
    
    return {"message": "Resume uploaded and parsed successfully", "user_id": user.id}
