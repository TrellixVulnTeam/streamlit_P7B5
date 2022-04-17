gcloud builds submit --tag gcr.io/streamlit-346103/streamlit --project==streamlit-346103
gcloud run deploy --image gcr.io/ee-richarchi1806/streamlit --platform managed --project==ee-richarchi1806 --allow-unauthenticated
