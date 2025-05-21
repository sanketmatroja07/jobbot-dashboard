from docx import Document
import os

def replace_keywords_in_resume(input_path, output_path, keyword_list):
    doc = Document(input_path)
    keywords_str = ', '.join(keyword_list)

    for para in doc.paragraphs:
        if '{KEYWORDS}' in para.text:
            para.text = para.text.replace('{KEYWORDS}', keywords_str)

    doc.save(output_path)
    print(f"[+] Resume customized and saved to: {output_path}")


# Test script usage
if __name__ == "__main__":
    test_keywords = ["Python", "SQL", "ETL", "AWS"]
    input_resume = "resume/resume_template.docx"
    output_resume = "resume/custom_resume.docx"

    replace_keywords_in_resume(input_resume, output_resume, test_keywords)
