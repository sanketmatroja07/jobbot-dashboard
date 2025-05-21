import openai
import os
import json

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY").strip())

def detect_form_fields(html_source):
    prompt = f"""
You are an intelligent HTML form parser AI. The HTML below contains a job application form.

Your task is to detect and return a JSON object with the best form field selectors for:
- Full Name
- Email
- Resume Upload
- Cover Letter
- Submit Button

Format each selector like one of these:
- "name=full_name" → for input with name="full_name"
- "id=email" → for input with id="email"
- "xpath=//input[@type='file']"
- "tag=textarea"
- "xpath=//button[contains(text(), 'Submit')]" (for submit buttons)

If a field is not found, return null for it.

Here is the HTML (truncated):
{html_source[:8000]}
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    try:
        return json.loads(response.choices[0].message.content.strip())
    except Exception as e:
        print("[!] Failed to parse GPT output:", e)
        return {}
