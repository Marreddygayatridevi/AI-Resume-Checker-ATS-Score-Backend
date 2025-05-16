import faiss
import numpy as np
from langchain_openai import OpenAIEmbeddings

embedding_model = OpenAIEmbeddings()

def embed_chunks(chunks: list[str]):
    return embedding_model.embed_documents(chunks)

def build_faiss_index(chunks: list[str], ids: list[str]):
    vectors = embed_chunks(chunks)
    index = faiss.IndexIDMap(faiss.IndexFlatL2(len(vectors[0])))
    index.add_with_ids(np.array(vectors).astype("float32"), np.array(ids).astype("int64"))
    return index


