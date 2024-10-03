from flask import Flask, request, jsonify
from config import Config
from ocr import convert_image_to_text
import os

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/test', methods=["GET"])
def sayhallo():
    return jsonify(message="Sukses"), 200
  

@app.route('/api/v1/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({"error": "Tidak ada file yang ditemukan."}), 400
    
    file = request.files['image']
    print("File Diterima")
    
    if file.filename == '':
        return jsonify({"error": "Tidak ada file yang dipilih."}), 400

    # Simpan file ke folder uploads
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Proses gambar dan ambil teks
    extracted_text = convert_image_to_text(file_path)

    # Hapus file setelah diproses (opsional)
    os.remove(file_path)

    # Kembalikan hasil ekstraksi dalam format JSON
    return jsonify({"extracted_text": extracted_text})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
