from selenium import webdriver
from selenium.webdriver.common.by import By
from form_detector import detect_form_fields
import time

def get_selector(selector_str):
    """Returns Selenium selector type and value from a GPT-formatted string like 'name=email'."""
    if not selector_str:
        return None, None
    parts = selector_str.split("=", 1)
    if len(parts) != 2:
        return None, None
    key, value = parts
    if key == "name":
        return By.NAME, value
    elif key == "id":
        return By.ID, value
    elif key == "xpath":
        return By.XPATH, value
    elif key == "tag":
        return By.TAG_NAME, value
    else:
        return None, None

def apply_to_job(url, name, email, resume_path, cover_letter_text):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(4)

    html = driver.page_source
    fields = detect_form_fields(html)
    print("🤖 GPT returned selectors:", fields)

    try:
        # Name field
        method, value = get_selector(fields.get("name"))
        if method:
            driver.find_element(method, value).send_keys(name)

        # Email field
        method, value = get_selector(fields.get("email"))
        if method:
            driver.find_element(method, value).send_keys(email)

        # Resume file upload
        method, value = get_selector(fields.get("resume"))
        if method:
            driver.find_element(method, value).send_keys(resume_path)

        # Cover letter field
        method, value = get_selector(fields.get("cover_letter"))
        if method:
            driver.find_element(method, value).send_keys(cover_letter_text)

        print("[✅] Successfully auto-filled the job form!")
        input("🔍 Review and press Enter to close the browser...")
        driver.quit()

    except Exception as e:
        print("[❌] Error auto-filling:", e)
        driver.quit()
# Submit button
method, value = get_selector(fields.get("submit"))
if method:
    try:
        driver.find_element(method, value).click()
        print("[🚀] Auto-submitted successfully!")
    except Exception as e:
        print(f"[!] Found submit selector but failed to click: {e}")
else:
    print("[ℹ️] No submit button detected by GPT — skipped submission.")
