# app/controllers/image_controller.py
from flask import request, jsonify, current_app
from app.utils import convert2image, preprocess, parser
from app.models.image_model import ImageModel
import os

class ImageController:
    def process_image(self):
        print("request masuk")
        print(request.files)
        if 'images' not in request.files:
            return jsonify({"error": "Tidak ada file yang ditemukan."}), 400
        print("Ada file yang dikirim")
        files = request.files.getlist('images')
        print(f"{len(files)} File Diterima")
        print(files)

        if not files:
            return jsonify({"error": "Tidak ada file yang dipilih."}), 400
          
        results = []
        for file in files:
            if file.filename == '':
                return jsonify({"error": "Tidak ada file yang dipilih."}), 400

            # Simpan file ke folder uploads
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
            try:
                file.save(file_path)

                # Proses gambar dan ambil teks
                model = ImageModel(file_path)
                extracted_content = convert2image(model.file_path)

                # Hapus file setelah diproses (opsional)
                os.remove(file_path)

                # Parsing konten
                parsing = parser(extracted_content)

                # Simpan hasil untuk setiap file
                results.append(parsing)

            except Exception as e:
                return jsonify({"error": str(e)}), 500

        # Kembalikan hasil ekstraksi dalam format JSON
        return jsonify(results)