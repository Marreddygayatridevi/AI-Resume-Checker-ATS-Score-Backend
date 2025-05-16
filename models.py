
from sqlalchemy import Column, Integer, String, LargeBinary
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String)
    resume_pdf = Column(LargeBinary)  # PDF binary data
    phone = Column(String)
    github = Column(String)
    linkedin = Column(String)
    resume_text = Column(String)
