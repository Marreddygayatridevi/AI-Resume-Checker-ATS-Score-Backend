from fastapi import FastAPI
from routers import user, admin
from database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app first
app = FastAPI(
    title="Resume Screening API",
    description="Users upload resumes and admins manage/filter them.",
    version="1.0.0"
)

# Add CORS middleware after app creation
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # <-- or ["*"] for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create all database tables
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
