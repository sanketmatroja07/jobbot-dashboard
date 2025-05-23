import json
import time
import sqlite3
from datetime import datetime
from job_scraper import get_simplify_jobs
from indeed_scraper import get_indeed_jobs
from remoteok_scraper import get_remoteok_jobs
from cover_letter_generator import generate_cover_letter
from resume_modifier import replace_keywords_in_resume
from app_tracker import has_applied, log_application
from auto_apply import apply_to_job

# ------------ LOGGING RUN RESULTS -------------
def log_run(success, message):
    conn = sqlite3.connect("run_log.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            success INTEGER,
            message TEXT
        )
    ''')
    cursor.execute(
        "INSERT INTO runs (timestamp, success, message) VALUES (?, ?, ?)",
        (datetime.utcnow().isoformat(), int(success), message[:500])
    )
    conn.commit()
    conn.close()

# ------------ MAIN APPLICATION AGENT -------------
try:
    # Load config
    with open("config.json", "r") as f:
        config = json.load(f)

    max_apps = config.get("max_daily_applications", 100)
    applied_count = 0

    # STEP 1: Get jobs from Simplify, Indeed, RemoteOK
    print("🔍 Fetching job listings from Simplify, Indeed, and RemoteOK...")
    simplify_jobs = get_simplify_jobs(config["target_titles"], config["locations"])
    indeed_jobs = get_indeed_jobs(config["target_titles"], config["locations"])
    remoteok_jobs = get_remoteok_jobs(config["target_titles"])

    # Tag each job with its platform
    for job in simplify_jobs:
        job["platform"] = "Simplify"
    for job in indeed_jobs:
        job["platform"] = "Indeed"
    for job in remoteok_jobs:
        job["platform"] = "RemoteOK"

    # Combine all jobs into one list
    jobs = simplify_jobs + indeed_jobs + remoteok_jobs
    print(f"📦 Total jobs loaded: {len(jobs)}")

    for job in jobs:
        if applied_count >= max_apps:
            break

        url = job["url"]
        company = job["company"]
        role = job["title"]
        job_desc = job["description"]
        platform = job.get("platform", "Unknown")

        if has_applied(url):
            print(f"🔁 Already applied to {company} - {role} ({platform})")
            continue

        # STEP 2: Generate custom cover letter
        print(f"✍️ Generating cover letter for {company} - {role} ({platform})")
        cover_letter = generate_cover_letter(company, role, job_desc)

        # STEP 3: Customize resume with smart keywords
        keywords = config["default_keywords"]
        replace_keywords_in_resume(
            input_path="resume/resume_template.docx",
            output_path="resume/custom_resume.docx",
            keyword_list=keywords
        )

        # STEP 4: Auto-fill and apply via AI-form detection
        print(f"🚀 Applying to {company} - {role} ({platform})")
        try:
            apply_to_job(
                url=url,
                name="Sanket Matroja",
                email="sanketmatroja07@gmail.com",
                resume_path="resume/custom_resume.docx",
                cover_letter_text=cover_letter
            )
            log_application(company, role, url)
            applied_count += 1
            time.sleep(3)
        except Exception as apply_err:
            print(f"[⚠️] Failed to apply to {company}: {apply_err}")
            continue

    log_run(True, f"✅ Successfully applied to {applied_count} jobs.")
    print("🎯 Job run completed successfully.")

except Exception as e:
    log_run(False, f"❌ Job run failed: {str(e)}")
    print(f"💥 Critical failure: {e}")
    raise
