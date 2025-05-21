import openai
from docx import Document
import os

# ✅ Set up the client correctly for openai>=1.0.0
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY").strip())


def generate_cover_letter(company, role, job_desc, user_name="Sanket Matroja"):
    prompt = f"""
    Write a concise, professional cover letter for a candidate named {user_name} applying to the role of '{role}' at {company}.
    Refer to the job description below to tailor the letter.

    Job Description:
    {job_desc}

    The candidate is pursuing a Master's in Computer Science and has skills in Python, SQL, AWS, GCP, and data engineering.
    Keep the tone enthusiastic yet professional. Limit to 250 words.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()

def save_to_docx(text, filename):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(filename)
    print(f"[+] Cover letter saved to: {filename}")

# 🔍 Test usage
if __name__ == "__main__":
    company = "Spotify"
    role = "Data Analyst Intern"
    job_desc = "Assist with data cleaning, dashboard creation, and ad-hoc reporting using SQL and Python."

    letter = generate_cover_letter(company, role, job_desc)
    save_to_docx(letter, "cover_letters/spotify_cover_letter.docx")
