from flask import request, jsonify, current_app
from app.utils import convert2image, formatting
from app.models.image_model import ImageModel
import os

test_response = {
    "error": [],
    "results": [
        {
            "closed": "Sudah dilakukan blocking IP Source untuk Sophos IPS pada firewall Sophos BGR, JTN dan PTM dengan detail IP 139.59.37.187",
            "content": "Detection : Telkomsat- Sophos IPS\nSource IP : 139.59.37.187\nSource Abuse % : 100\nSource ISP : DigitalOcean LLC\nSource Location : India\nSource Network : other\nDestination IP : 10.80.253.47\nDestination Network : Bogor\nDestination Port : 80 (100.0%)\nLog Subtype : Drop\nURL Category: scan\nsignature msg : SCAN Zgrab Scanning Attempt Detected\nFirewall rule name: LibreNMS\nEvent Count: 2\nLog Source : Telkomsat.SophosFW\nWaktu Kejyadian : 04 Oct 2024 22:17:07\n",
            "title": "Sophos IPS 139.59.37.187"
        },
        {
            "closed": "Sudah dilakukan blocking IP Source untuk Web App Attack pada firewall Check Point dengan detail IP 116.55.72.22 188.166.224.80",
            "content": "Detection : Telkomsat - Web App Attack Vv\nSource IP : 116.55.72.22\nSource Abuse % : 100\nSource ISP : ChinaNet Yunnan Province Network\nSource Location : China\nSource Network : other\nDestination IP : 10.80.253.102\nDestination Network : Bogor\nCP Action: Alert_Deny\nCP Severity : High\nDestination Hostname : www.telkomsat.co.id\nURL : 45.126.155.10:443\nURL Path: /cgi-bin/../../../.././../.././.-/./bin/sh\nUser Agent : Custom-AsyncHttpClient\nhttp method : post\nThreat Level : Severe\nSignature subclass : Command Injection\nowasp top10 : A03:2021-Injection\nEvent Count: 2\nLog Source : Telkomsat.Fortiweb\nWaktu Kejadian : 04 Oct 2024 04:24:11\n\nDetection : Telkomsat - Web App Attack\nSource IP : 188.166.224.80\nSource Abuse % : 22\nSource ISP : DigitalOcean LLC\nSource Location : Singapore\nSource Network : other\nDestination IP : 10.80.253.102\nDestination Network : Bogor\nCP Action: Alert_Deny, notice\nCP Severity : High\nDestination Hostname : www.telkomsat.co.id\nURL : www.telkomsat.co.id\nURL Path : /.quarantine/ALFA_DATA/alfacgiapi/404.php?bx=0e2 15962017,\n/.quarantine/ALFA_DATA/alfacgiapt/bash.alfa, /.quarantine/ALFA_DATA/alfacgiapi/index.php?\nbx=0e215962017\nUser Agent : Mozilla/5.0 (Linux: Android 11; Redmi Note 9 Pro Build/RKQ1.200826.002: wv)\nAppleWebkKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/90.0.4430.210 Mobile Safan/537.36,\nMozlila/5.0 (Linux: Android 7.0; SM-G892A Bulid/NRD90M; wv) AppleWebKit/537.36 (KHTML like\nGecko) Version/4.0 Chrome/60.0.3112.107 Moblie Safar/537.36\nhttp method : get. post\nThreat Level : Substantial\nSignature subclass : Signatures for Common Web Applications\nowasp top10: A06:2021-Vulnerable and Outdated Components\nEvent Count : 2115\nLog Source : Telkomsat.Fortiweb\nWaktu Kejyadian : 04 Oct 2024 04:47:33\n",
            "title": "Web App Attack 116.55.72.22 188.166.224.80"
        }
    ]
}

class ImageController:
    def process_image(self):
        # return test_response
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
        # return result