import os, requests

SUPA_URL = os.getenv("SUPA_URL")
SUPA_SERVICE_KEY = os.getenv("SUPA_SERVICE_KEY")
BUCKET = os.getenv("SUPA_BUCKET", "contracts-bucket")

def download_file(file_path: str) -> bytes:
    url = f"{SUPA_URL}/storage/v1/object/{BUCKET}/{file_path}"
    r = requests.get(url, headers={"apikey": SUPA_SERVICE_KEY, "Authorization": f"Bearer {SUPA_SERVICE_KEY}"})
    r.raise_for_status()
    return r.content

def patch_request(req_id: str, payload: dict):
    url = f"{SUPA_URL}/rest/v1/requests?id=eq.{req_id}"
    r = requests.patch(url, json=payload, headers={"apikey": SUPA_SERVICE_KEY, "Authorization": f"Bearer {SUPA_SERVICE_KEY}"})
    r.raise_for_status()
