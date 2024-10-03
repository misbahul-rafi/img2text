import os

class Config:
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  # Folder untuk menyimpan gambar
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Maksimal ukuran file 16MB
