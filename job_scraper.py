import requests
import json
from fake_useragent import UserAgent

def get_simplify_jobs(title_keywords, locations):
    url = "https://api.simplify.jobs/feed/jobs"
    headers = {
        "User-Agent": UserAgent().random,
        "Content-Type": "application/json"
    }

    jobs_found = []

    for title in title_keywords:
        for loc in locations:
            payload = {
                "query": f"{title} {loc}",
                "filters": {},
                "limit": 25
            }

            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                jobs = response.json().get("jobs", [])
                for job in jobs:
                    job_data = {
                        "title": job.get("title"),
                        "company": job.get("companyName"),
                        "location": job.get("location"),
                        "url": job.get("url"),
                        "description": job.get("description", "")[:300]
                    }
                    jobs_found.append(job_data)

    return jobs_found

# Test block
if __name__ == "__main__":
    sample_jobs = get_simplify_jobs(["Data Analyst Intern"], ["Remote"])
    for job in sample_jobs[:5]:
        print(job["title"], "-", job["company"])
        print(job["url"])
        print("---")
