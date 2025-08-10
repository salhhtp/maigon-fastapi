# Maigon FastAPI Services

- One FastAPI microservice per contract type.
- Expects env: `SUPA_URL`, `SUPA_SERVICE_KEY`, `SUPA_BUCKET`.

## Build & Deploy (example for DPA)
gcloud builds submit --tag gcr.io/<project>/dpa:latest -f services/Dockerfile.gpu
gcloud run deploy dpa-review --image gcr.io/<project>/dpa:latest --region europe-west4 --gpu=1 --cpu=8 --memory=16Gi --allow-unauthenticated
