"""Firebase configuration for Adaptive Narrative Engine."""

import os
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import Client


# Initialize Firebase Admin SDK
def initialize_firebase() -> Client:
    """Initialize Firebase Admin SDK"""
    if not firebase_admin._apps:
        # Check for service account credentials
        service_account_path = os.getenv("CREDENTIALS_PATH")

        if service_account_path and os.path.exists(service_account_path):
            cred = credentials.Certificate(service_account_path)
            app = firebase_admin.initialize_app(credential=cred)
        else:
            # Use default credentials (for Cloud Run or local emulator)
            # When testing locally without credentials, this will fail unless GOOGLE_APPLICATION_CREDENTIALS is set
            try:
                app = firebase_admin.initialize_app()
            except ValueError:
                # App already exists or default credentials not found, initialize dummy app for testing
                app = firebase_admin.initialize_app(options={'projectId': 'demo-project'})

    return firestore.client(app=app)

# Global Firestore client
db = initialize_firebase()
