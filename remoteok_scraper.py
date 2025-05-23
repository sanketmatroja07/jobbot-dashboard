import requests

def get_remoteok_jobs(keywords):
    job_results = []
    try:
        response = requests.get("https://remoteok.com/api")
        if response.status_code != 200:
            print("[RemoteOK] Failed to fetch jobs")
            return []

        jobs = response.json()[1:]  # Skip first metadata object

        for job in jobs:
            position = job.get("position") or job.get("title", "")
            company = job.get("company", "")
            url = job.get("url", "")
            description = job.get("description", "")[:300]

            for keyword in keywords:
                if keyword.lower() in position.lower():
                    job_results.append({
                        "title": position,
                        "company": company,
                        "url": url,
                        "description": description,
                        "platform": "RemoteOK"
                    })
                    break

        return job_results

    except Exception as e:
        print(f"[RemoteOK] Error: {e}")
        return []
