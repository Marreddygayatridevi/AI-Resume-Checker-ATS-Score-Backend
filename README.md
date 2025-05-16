# 💼 Resume Screening Backend (FastAPI + LangChain + FAISS)

A powerful backend service for AI-powered resume screening. Built with **FastAPI**, **PostgreSQL**, **FAISS**, and **LangChain + OpenAI**, this backend handles resume uploads, parsing, job-role based filtering, and give ATS Score for  resumes based on relevance.

---

## 🚀 Features

* ✅ User registration and resume PDF upload
* ✅ Resume parsing with contact extraction (email, phone, GitHub, LinkedIn)
* ✅ Intelligent ATS scoring using OpenAI embeddings and FAISS
* ✅ Admin-only screening dashboard
* ✅ Admin resume viewer (in-browser PDF)
* ✅ Dynamic job-role descriptions from text files
* ✅ Scalable architecture using PostgreSQL and FAISS

---

## 🧰 Tech Stack

| Component      | Technology                    |
| -------------- | ----------------------------- |
| Backend        | FastAPI, Uvicorn              |
| ORM            | SQLAlchemy                    |
| Database       | PostgreSQL (resumes in bytea) |
| Vector Search  | FAISS                         |
| LLM            | OpenAI GPT-4 via LangChain    |
| Embeddings     | OpenAIEmbeddings              |
| Resume Parsing | PyMuPDF + Regex               |

---

## 📁 Project Structure

```bash
backend/app/
├── jobroles/                     # .txt files with job descriptions
│   ├── DataAnalyst.txt
│   ├── softwaredeveloper.txt
│   └── ...
├── routers/
│   ├── admin.py                  # Admin routes
│   └── user.py                   # User routes
├── database.py                   # PostgreSQL DB setup
├── main.py                       # FastAPI entry point
├── models.py                     # SQLAlchemy models
├── requirements.txt              # Python dependencies
├── resume_parser.py              # PyMuPDF + regex parser
├── vectordb.py                   # FAISS index creation/loading
└── vectorembeddings.py           # Resume-job ATS scoring
```

---

## ⚙️ Setup Instructions

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/resume-screening-backend.git
cd resume-screening-backend/backend/app
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
   Create a `.env` file:

```env
DATABASE_URL=postgresql+psycopg2://user:password@localhost/dbname
OPENAI_API_KEY=sk-...
```

4. **Run the server:**

```bash
uvicorn main:app --reload
```

---

## 🔌 API Endpoints

### 👤 User Endpoints

* `POST /register/`

  * Register a new user with resume PDF
* `GET /resume/{user_id}`

  * Retrieve resume PDF by user ID

### 🔐 Admin Endpoints

* `POST /admin/login/`

  * Login as admin using `name=admin`, `password=kaaylabs`
* `GET /admin/users/?role=...`

  * List all users, optionally filtered by role
* `GET /admin/faiss-process/?role=...`

  * Perform ATS scoring and return top 7 matching resumes
* `GET /admin/list-jobroles`

  * List all available job roles (based on `jobroles/` folder)
* `GET /admin/resume/pdf/{user_id}`

  * Fetch and view resume PDF for a specific user

---

## ✅ Admin ATS Matching Logic

1. Admin selects job role (from list generated from `jobroles/*.txt`)
2. Matching resumes (with that role) are retrieved from DB
3. Each resume is parsed and embedded using OpenAI
4. Resume embeddings are compared to job role embedding via FAISS
5. Top 7 matches are returned with ATS score, name, and email

---

## 🔒 Authentication

* Admin access is gated using simple login credentials (`admin` / `kaaylabs`)
* Session is maintained using a global flag (can be improved with OAuth/JWT)

---



## ✍ Author

Made with ❤ by **Marreddy Gayatri Devi**

---

## 📜 License

This project is released for **personal and educational use only**. All rights reserved by *Marreddy Gayatri Devi*.
