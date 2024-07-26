import firebase_admin
from firebase_admin import credentials, firestore, storage
from google.api_core.exceptions import GoogleAPIError

# Initialize Firebase Admin SDK
def initialize_firebase():
    try:
        cred = credentials.Certificate('serviceAccountKey.json')
        firebase_admin.initialize_app(cred, {
            'storageBucket': 'phishing-analyzer-cbac8.appspot.com'
        })
        print("Firebase initialized successfully.")
    except Exception as e:
        print(f"Error initializing Firebase: {e}")

initialize_firebase()

db = firestore.client()
bucket = storage.bucket()

def upload_image_and_get_url(image_path, destination_blob_name):
    try:
        # Uploads an image to the bucket and returns the public URL of the image
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(image_path)
        blob.make_public()
        return blob.public_url
    except GoogleAPIError as e:
        print(f"Google API Error during upload: {e}")
    except Exception as e:
        print(f"Error during upload: {e}")

def save_image_url_to_firestore(doc_id, image_url):
    try:
        # Save the image URL to Firestore
        doc_ref = db.collection('images').document(doc_id)
        doc_ref.set({'image_url': image_url})
        print("Image URL saved to Firestore successfully.")
    except GoogleAPIError as e:
        print(f"Google API Error while saving to Firestore: {e}")
    except Exception as e:
        print(f"Error saving to Firestore: {e}")
