gcloud builts submit --tag gcr.io/ee-richarchi1806/streamlit --project==ee-richarchi1806
gcloud run deploy --image gcr.io/ee-richarchi1806/streamlit --platform managed --project==ee-richarchi1806 --allow-unauthenticated
