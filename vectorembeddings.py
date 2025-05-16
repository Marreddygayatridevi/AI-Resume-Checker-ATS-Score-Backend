from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

def analyze_resumes(resume_texts, job_txt_text, user_ids):
    # Step 1: Convert resumes to documents
    documents = [Document(page_content=txt) for txt in resume_texts]

    # Step 2: Initialize embedding model
    embedding_model = OpenAIEmbeddings()

    # Step 3: Create FAISS index
    faiss_vectorstore = FAISS.from_documents(documents, embedding_model)

    # Step 4: Embed the job description
    job_embedding = embedding_model.embed_query(job_txt_text)

    # Step 5: Compute similarity between job description and each resume
    # Get vectors from FAISS index
    resume_vectors = [faiss_vectorstore.index.reconstruct(i) for i in range(len(documents))]

    # Compute cosine similarities
    def cosine_similarity(vec1, vec2):
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    scores = []
    for i, vec in enumerate(resume_vectors):
        score = cosine_similarity(vec, job_embedding)
        scores.append((user_ids[i], score))

    # Step 6: Sort by score and return top 5
    top_matches = sorted(scores, key=lambda x: x[1], reverse=True)[:7]

    return {
        "top_matches": [
            {
                "resume_id": rid,
                "ats_score": round(score * 100, 2)
            }
            for rid, score in top_matches
        ]
    }


