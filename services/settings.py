import os
from dotenv import load_dotenv

load_dotenv()

env = os.getenv

CLOUDINARY_CLIENT_NAME = env("CLOUDINARY_CLIENT_NAME")
CLOUDINARY_API_KEY = env("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = env("CLOUDINARY_API_SECRET")