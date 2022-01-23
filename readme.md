gcloud builts submit --tag gcr.io/ubicacion-284517/streamlit --project==ubicacion-284517
gcloud run deploy --image gcr.io/ubicacion-284517/streamlit --platform managed --project==ubicacion-284517 --allow-unauthenticated
