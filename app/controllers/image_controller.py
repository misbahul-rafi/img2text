from flask import request, jsonify, current_app
from app.utils import convert2image, formatting
from app.models.image_model import ImageModel
import os


class ImageController:
    def process_image(self):
        if "images" not in request.files:
            print(request.files)
            return jsonify({"error": "Tidak ada file yang ditemukan."}), 400
        files = request.files.getlist("images")
        if not files:
            return jsonify({"error": "Tidak ada file yang dipilih."}), 400
        result = []
        for file in files:
            if file.filename == "":
                return jsonify({"error": "Tidak ada file yang dipilih."}), 400
            file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], file.filename)
            try:
                file.save(file_path)
                model = ImageModel(file_path)
                extracted_content = convert2image(model.file_path)
                os.remove(file_path)
                if extracted_content:
                    result.append(extracted_content)
                    print("lanjut")
                else:
                    return jsonify({"error": "Tidak ada konten yang berhasil diekstrak dari gambar."}), 400
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        return formatting(result)