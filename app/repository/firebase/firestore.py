import firebase_admin
import os

# from firebase_admin import firestore
from google.cloud import firestore
from dotenv import load_dotenv

load_dotenv()


credentials = firebase_admin.credentials.Certificate(
    {
        "type": "service_account",
        "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
        "private_key": os.environ.get("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
        "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
        "token_uri": "https://oauth2.googleapis.com/token",
    }
)

firebase_app = firebase_admin.initialize_app(credentials)
db = firestore.Client()
