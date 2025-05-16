from fastapi import APIRouter, HTTPException, Depends, Form, Response
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from resume_parser import parse_resume
from vectorembeddings import analyze_resumes
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()
admin_authenticated = False

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login/")
def admin_login(name: str = Form(...), password: str = Form(...)):
    global admin_authenticated
    if name == "admin" and password == "kaaylabs":
        admin_authenticated = True
        return {"msg": "Admin authenticated"}
    raise HTTPException(status_code=401, detail="Invalid admin credentials")

@router.get("/users/")
def get_all_users(role: str = None, db: Session = Depends(get_db)):
    if not admin_authenticated:
        raise HTTPException(status_code=403, detail="Admin not authenticated")

    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    users = query.all()
    return [
        {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "role": u.role
        } for u in users
    ]

@router.get("/faiss-process/")
def match_users(role: str, db: Session = Depends(get_db)):
    if not admin_authenticated:
        raise HTTPException(status_code=403, detail="Admin not authenticated")

    job_txt_path = Path(f"jobroles/{role}.txt")
    if not job_txt_path.exists():
        raise HTTPException(status_code=404, detail="Job role description not found.")
    job_txt_text = job_txt_path.read_text()

    users = db.query(User).filter(User.role == role).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found for this role")

    resume_texts = [user.resume_text for user in users]
    user_ids = [user.id for user in users]

    result = analyze_resumes(resume_texts, job_txt_text, user_ids)

    # Enrich the top matches with user info
    top_matches = result.get("top_matches", [])
    enriched_matches = []
    for match in top_matches:
        user = db.query(User).filter(User.id == match["resume_id"]).first()
        if user:
            enriched_matches.append({
                "user_id": user.id,
                "name": user.name,
                "email": user.email,
                "ats_score": match["ats_score"]
            })

    return {"top_7_resumes": enriched_matches}

@router.get("/list-jobroles")
def list_job_roles():
    jobroles_folder = os.path.join(os.path.dirname(__file__), "../jobroles")
    if not os.path.exists(jobroles_folder):
        raise HTTPException(status_code=200, detail="Job roles folder not found")

    job_roles = [f[:-4] for f in os.listdir(jobroles_folder) if f.endswith(".txt")]
    return {"roles": job_roles}

@router.get("/resume/pdf/{user_id}")
def get_resume_pdf(user_id: int, db: Session = Depends(get_db)):
    if not admin_authenticated:
        raise HTTPException(status_code=403, detail="Admin not authenticated")

    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.resume_pdf:
        raise HTTPException(status_code=404, detail="PDF not found")

    headers = {
        "Content-Disposition": f'inline; filename="resume_{user_id}.pdf"'
    }

    return Response(content=user.resume_pdf, media_type="application/pdf", headers=headers)


