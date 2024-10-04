from flask import request, jsonify, current_app
from app.utils import convert2image, formatting
from app.models.image_model import ImageModel
import os
import json


class ImageController:
    def process_image(self):
    #     text = {
    #     "closed": [
    #         "Sudah dilakukan blocking IP Address untuk Sophos IPS pada firewall Sophos dengan IP Source 139.59.37.187",
    #         "Sudah dilakukan blocking IP Address untuk Web Scanner By URL Path pada firewall CheckPoint dengan IP Source 146.190.104.144"
    #     ],
    #     "content": [
    #         "Detection : Telkomsat- Sophos IPS\n\nSource IP : 139.59.37.187\n\nSource Abuse % : 100\n\nSource ISP : DigitalOcean LLC\n\nSource Location : India\n\nSource Network : other\n\nDestination IP : 10.80.253.47\n\nDestination Network : Bogor\n\nDestination Port : 80 (100.0%)\n\nLog Subtype : Drop\n\nURL Category: scan\n\nsignature msg : SCAN Zgrab Scanning Attempt Detected\n\nFirewall rule name: LibreNMS\n\nEvent Count: 2\n\nLog Source : Telkomsat.SophosFW\n\nWaktu Kejyadian : 04 Oct 2024 22:17:07\n\nSummary : Source ip dengan bad reputation melakukan serangan dengan indikasi tersebut\nRecommendation : Lakukan blacklist source IP tersebut pada ACL untuk mencegah serangan lebth\nlanjut\n\nNote: Source IP tersebut akan kami blacklist\n\nRisk and Impact : Upaya pemindaian vunerbility yang dilakukan oleh penyerang, hal ini bisa\nmenyebabkan attacker dapat memperoleh kendali pada sistem yang rentan. 22.25\n\f",
    #         "Detection : Telkomsat - Possible Web Scanner By URL Path\n\nSource IP : 146.190.104.144\n\nSource Abuse % : 4\n\nSource ISP : DigitalOcean LLC\n\nSource Location : Singapore\n\nSource Network : other\n\nDestination IP : 10.80.253.102\n\nCode : 200, 301, 302\n\nDestination Hostname : www.telkomsat.co.id\n\nPolicy Name: “N/A”, “WAF-Telkomsat”\n\nStatus Code : “Disabled”, success\n\nType : attack, traffic\n\nURL : www.telkomsat.co.id\n\nURL Path: /1.php, /3index.php ?f=/NmRtvOUjAdutReQy/scRyKUhleBpzmTyO.txt, /ALFA_DATA\n\nUser Agent : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko)\nChrome/90.0.4430.85 Safari/537.36, wp_is_mobile\n\nhttp method : get. post\n\nWaktu Kejadian : 04 Oct 2024 02:16:58\n\nLog Source : Telkomsat.Fortiweb\n\nEvent Count : 210\n\nContainment : Traffic dari Source IP int indikasi web scanning ke destination hostname tersebut.\nLakukan pengecekan Source IP tersebut merupakan valid IP vulnerability manager atau bukan dan\nmemberitahu ke kami sehingga nantinya tidak akan muncul kembali alert ini. jika bukan\nmerupakan valid vulnerability manager, mohon untuk segera blok IP tersebut misalnya 2 jam atau\n1 hari di fortiweb.\n\nEradication : apabila tidak valid vulnerability manager. diskusikan kepada team fortiweb, untuk\ndapat melakukan auto block jika suatu ip dianggap melakukan scanning dengan kondisi tertentu.\nSource IP tersebut akan diblacklist pada Checkpoint. 02:21\n\f"
    #     ],
    #     "error": [],
    #     "title": [
    #         "Sophos IPS 139.59.37.187",
    #         "Web Scanner By URL Path 146.190.104.144"
    #     ]
    # }
    #     return text
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
                else:
                    return jsonify({"error": "Tidak ada konten yang berhasil diekstrak dari gambar."}), 400
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        return formatting(result)