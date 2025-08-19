# app/routers/webhooks.py
from fastapi import APIRouter, Request, Header, HTTPException
import stripe
from app.config import settings

router = APIRouter(prefix="/webhooks", tags=["webhooks"])
stripe.api_key = settings.STRIPE_SECRET_KEY


@router.post("/stripe")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    payload = await request.body()
    sig_header = stripe_signature
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    # handle event types
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        # TODO: fetch session.client_reference_id or metadata to update subscription
        # write to transactions table, update subscriptions
    elif event["type"].startswith("invoice"):
        pass
    # ... more events
    return {"received": True}
