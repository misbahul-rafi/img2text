import os

class Config:
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Maksimum ukuran file 16 MB

# Membuat folder uploads jika belum ada
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)