import os
from google.cloud import pubsub_v1

# ------------------------------
# Configuration
# ------------------------------
SERVICE_ACCOUNT_PATH = os.getenv(
    "FIREBASE_CREDENTIALS_PATH",  # can reuse your Firebase service account JSON
    "app/core/creds.json"
)

GCP_PROJECT = os.getenv("GCP_PROJECT", "kai-developer-test")
PUBSUB_TOPIC = os.getenv("PUBSUB_TOPIC", "process-text-task")
PUBSUB_SUBSCRIPTION = os.getenv("PUBSUB_SUBSCRIPTION", "process-text-sub")

# ------------------------------
# Detect if running in Cloud Run
# ------------------------------
RUNNING_IN_CLOUD_RUN = os.getenv("RUNNING_IN_CLOUD_RUN", "0") == "1"

# ------------------------------
# Initialize Pub/Sub clients
# ------------------------------
if RUNNING_IN_CLOUD_RUN:
    # Use Cloud Run default credentials
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
else:
    # Local development using service account JSON
    publisher = pubsub_v1.PublisherClient.from_service_account_file(SERVICE_ACCOUNT_PATH)
    subscriber = pubsub_v1.SubscriberClient.from_service_account_file(SERVICE_ACCOUNT_PATH)

# ------------------------------
# Resource paths
# ------------------------------
PUBSUB_TOPIC_PATH = publisher.topic_path(GCP_PROJECT, PUBSUB_TOPIC)
PUBSUB_SUBSCRIPTION_PATH = subscriber.subscription_path(GCP_PROJECT, PUBSUB_SUBSCRIPTION)
