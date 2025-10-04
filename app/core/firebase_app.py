import os
from firebase_admin import credentials, initialize_app, auth
from google.cloud import firestore as gcp_firestore

# # Path to Firebase service account
FIREBASE_CRED_PATH = os.getenv(
    "FIREBASE_CREDENTIALS_PATH",
    "app/core/creds.json"
)

# Firestore DB name (e.g. "projects/{project}/databases/{database_id}")
FIRESTORE_DB_NAME = os.getenv(
    "FIRESTORE_DB_NAME",
    "nsr-fs-db"
)

# Initialize Firebase Admin once
try:
    cred = credentials.Certificate(FIREBASE_CRED_PATH)
    default_app = initialize_app(cred)
except ValueError:
    from firebase_admin import get_app
    default_app = get_app()


# Use google-cloud-firestore directly
gcp_client = gcp_firestore.Client.from_service_account_json(
    FIREBASE_CRED_PATH,
    database=FIRESTORE_DB_NAME
)

# Shared services
firebase_auth = auth
firebase_db = gcp_client