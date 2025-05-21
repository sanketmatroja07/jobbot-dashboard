import json
import time
from job_scraper import get_simplify_jobs  # or another job scraper
from cover_letter_generator import generate_cover_letter
from resume_modifier import replace_keywords_in_resume
from app_tracker import has_applied, log_application
from auto_apply import apply_to_job

# Load config
with open("config.json", "r") as f:
    config = json.load(f)

# Init variables
MAX_APPLICATIONS = config.get("max_daily_applications", 100)
applied_count = 0

# 🔁 Step 1: Get jobs
jobs = get_simplify_jobs(config["target_titles"], config["locations"])

for job in jobs:
    if applied_count >= MAX_APPLICATIONS:
        break

    url = job["url"]
    company = job["company"]
    role = job["title"]
    job_desc = job["description"]

    if has_applied(url):
        continue

    # 🔁 Step 2: Generate cover letter
    cover_letter_text = generate_cover_letter(company, role, job_desc)

    # 🔁 Step 3: Customize resume with relevant keywords
    replace_keywords_in_resume(
        input_path="resume/resume_template.docx",
        output_path="resume/custom_resume.docx",
        keyword_list=config["default_keywords"]
    )

    # 🔁 Step 4: Launch browser and apply
    try:
        apply_to_job(
            url=url,
            name="Sanket Matroja",
            email="sanketmatroja07@gmail.com",
            resume_path="resume/custom_resume.docx",
            cover_letter_text=cover_letter_text
        )
        log_application(company, role, url)
        applied_count += 1
        time.sleep(5)  # Wait between applications

    except Exception as e:
        print(f"[!] Failed to apply to {company} – {e}")
