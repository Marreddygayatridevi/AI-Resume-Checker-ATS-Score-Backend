# import fitz  # PyMuPDF
# import re
# from typing import Dict, List

# # ---- Full Resume Extraction ----
# def extract_full_resume_content(pdf_file: bytes) -> Dict:
#     doc = fitz.open(stream=pdf_file, filetype="pdf")

#     all_text = ""
#     all_links = []
#     pages = []

#     for page_num, page in enumerate(doc, start=1):
#         text = page.get_text()
#         all_text += text + "\n"

#         links = [link['uri'] for link in page.get_links() if 'uri' in link]
#         all_links.extend(links)

#         pages.append({
#             "page_number": page_num,
#             "text": text,
#             "links": links
#         })

#     metadata = doc.metadata
#     doc.close()

#     return {
#         "text": all_text.strip(),
#         "hyperlinks": list(set(all_links)),
#         "pages": pages,
#         "metadata": metadata
#     }

# # ---- Field Extractors ----
# def extract_email(text: str) -> str:
#     match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
#     return match.group(0) if match else ""

# def extract_phone(text: str) -> str:
#     match = re.search(r'\+?\d[\d\s\-\(\)]{8,}\d', text)
#     return match.group(0) if match else ""

# def extract_linkedin(links: List[str], text: str) -> str:
#     for link in links:
#         if "linkedin.com/in" in link:
#             return link.strip()
#     match = re.search(r'linkedin[:\s]+([a-zA-Z0-9\-_./]+)', text, re.IGNORECASE)
#     if match:
#         return f"https://www.linkedin.com/in/{match.group(1).strip()}"
#     return ""

# def extract_github(links: List[str], text: str) -> str:
#     for link in links:
#         if re.match(r'https?://[a-zA-Z0-9\-]+\.github\.io/$', link):
#             return link.strip()

#     for link in links:
#         if re.match(r'https?://[a-zA-Z0-9\-]+\.github\.io(/[A-Za-z0-9\-]*)?$', link):
#             return link.strip()

#     for link in links:
#         match = re.match(r'https?://github\.com/([a-zA-Z0-9\-]+)(/?$)', link.strip("/"))
#         if match:
#             return f"https://github.com/{match.group(1)}"

#     match = re.search(r'github[:\s]+([a-zA-Z0-9\-_]+)', text, re.IGNORECASE)
#     if match:
#         return f"https://github.com/{match.group(1).strip()}"

#     return ""

# # ---- Resume Parser Interface ----
# def parse_resume(pdf_file: bytes) -> Dict:
#     resume_data = extract_full_resume_content(pdf_file)

#     email = extract_email(resume_data['text'])
#     phone = extract_phone(resume_data['text'])
#     github = extract_github(resume_data['hyperlinks'], resume_data['text'])
#     linkedin = extract_linkedin(resume_data['hyperlinks'], resume_data['text'])

#     return {
#         "email": email,
#         "phone": phone,
#         "github": github,
#         "linkedin": linkedin,
#         "resume_text": resume_data['text'],
#         "hyperlinks": resume_data['hyperlinks'],
#         "metadata": resume_data['metadata'],
#     }
import fitz  # PyMuPDF
import re
from typing import Dict, List

# --- Text Extraction ---
def extract_full_resume_content(pdf_file: bytes) -> Dict:
    """Extract full text, hyperlinks, and metadata from a PDF file."""
    with fitz.open(stream=pdf_file, filetype="pdf") as doc:
        text = "\n".join([page.get_text() for page in doc])
        links = [link['uri'] for page in doc for link in page.get_links() if 'uri' in link]
        metadata = doc.metadata

    return {
        "text": text.strip(),
        "hyperlinks": list(set(links)),
        "metadata": metadata
    }

# --- Contact Extraction ---
def extract_email(text: str) -> str:
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0).strip() if match else ""

def extract_phone(text: str) -> str:
    match = re.search(r'(\+?\d[\d\s\-\(\)]{8,}\d)', text)
    return match.group(0).strip() if match else ""

# --- Profile Links ---
def extract_profile_link(links: List[str], keyword: str) -> str:
    for link in links:
        if keyword in link.lower():
            return link.strip()
    return ""

# --- Skills Extraction ---
def extract_skills(text: str) -> List[str]:
    known_skills = {
        "Python", "Java", "C++", "React", "SQL", "FastAPI", "Django",
        "Machine Learning", "Data Science", "AWS", "Git", "Linux",
        "Docker", "HTML", "CSS", "JavaScript", "TensorFlow", "Keras"
    }
    # Normalize text for matching
    text_lower = text.lower()
    return [skill for skill in known_skills if skill.lower() in text_lower]

# --- Experience & Education Sections ---
def extract_section(text: str, section_keywords: List[str], max_chars: int = 500) -> str:
    pattern = r'(?i)(' + '|'.join(re.escape(word) for word in section_keywords) + r')[:\s]*([\s\S]{0,' + str(max_chars) + r'})'
    match = re.search(pattern, text)
    return match.group(0).strip() if match else ""

# --- Main Parser ---
def parse_resume(pdf_file: bytes) -> Dict:
    content = extract_full_resume_content(pdf_file)
    text = content['text']
    links = content['hyperlinks']

    return {
        "email": extract_email(text),
        "phone": extract_phone(text),
        "github": extract_profile_link(links, "github.com"),
        "linkedin": extract_profile_link(links, "linkedin.com/in"),
        "resume_text": text,
        "hyperlinks": links,
        "metadata": content['metadata'],
        "skills": extract_skills(text),
        "experience": extract_section(text, ["experience", "work experience"]),
        "education": extract_section(text, ["education", "academic background"]),
    }
