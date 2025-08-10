from fastapi import FastAPI
from pydantic import BaseModel
from common.supa import download_file, patch_request
import json

app = FastAPI()

class ReviewReq(BaseModel):
    request_id: str
    file_path: str

def analyze_contract(raw_bytes: bytes) -> dict:
    # TODO: replace with your real model call (SpaCy/HF/etc.)
    text = raw_bytes[:2000].decode(errors="ignore")
    return {"summary": "OK", "sample": text[:200]}

@app.post("/review")
def review(payload: ReviewReq):
    patch_request(payload.request_id, {"status":"running"})
    data = download_file(payload.file_path)
    result = analyze_contract(data)
    patch_request(payload.request_id, {"status":"done", "result_json": result})
    return {"ok": True}
