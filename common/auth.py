import hmac, hashlib, os
def verify_sig(payload: str, header_sig: str) -> bool:
    key = os.getenv("GPU_HMAC_SECRET","").encode()
    mac = hmac.new(key, payload.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(header_sig, mac)
