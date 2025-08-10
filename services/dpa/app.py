from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from common.supa import patch_request
from common.auth import verify_sig
import requests, os

app = FastAPI()

class ReviewReq(BaseModel):
    request_id: str
    signed_url: str
    service_code: str

def analyze_contract(raw: bytes) -> dict:
    # TODO: plug your real model; return unified schema
    return {
      "serviceCode": "dpa", "overallRisk": 12,
      "findings": [], "metadata": {"length": len(raw)}
    }

@app.post("/review")
def review(p: ReviewReq, x_signature: str = Header(...)):
    if not verify_sig(p.signed_url, x_signature):
        raise HTTPException(status_code=403, detail="bad signature")
    patch_request(p.request_id, {"status":"running"})
    data = requests.get(p.signed_url).content
    result = analyze_contract(data)
    patch_request(p.request_id, {"status":"done", "result_json": result})
    return {"ok": True}
