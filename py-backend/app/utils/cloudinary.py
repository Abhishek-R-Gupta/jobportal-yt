import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# Utility function to upload files
def upload_to_cloudinary(file_content):
    try:
        result = cloudinary.uploader.upload(file_content)
        return result
    except Exception as e:
        print(f"Cloudinary upload error: {e}")
        return None
