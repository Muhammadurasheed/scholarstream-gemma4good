
import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

load_dotenv()

if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()
docs = db.collection('scholarships').order_by('last_verified', direction=firestore.Query.DESCENDING).limit(5).stream()

print("Latest 5 scholarships in Firestore:")
for doc in docs:
    data = doc.to_dict()
    print(f"- {data.get('title') or data.get('name')} (Source: {data.get('source_type')}, Verified: {data.get('last_verified')})")
