import re


def parser(input_text):
    data = {}
    lines = input_text.strip().split("\n")

    # Menyimpan isi asli
    original_content = []

    for line in lines:
        if line.startswith("Containment"):
            break

        # Mengumpulkan isi asli
        original_content.append(line)

        if "Source IP" in line:
            ip_match = re.search(r"Source IP : (\d+\.\d+\.\d+\.\d+)", line)
            if ip_match:
                data["ip"] = ip_match.group(1)

        if "Detection" in line:
            detection_match = re.search(r"Detection : (.+)", line)
            if detection_match:
                data["title"] = detection_match.group(1).strip()

    # Menggabungkan semua isi menjadi string
    combined_content = "\n".join(original_content)
    data["content"] = re.sub(r'\n{2,}', '\n', combined_content)

    # Mengubah format output sesuai dengan yang diminta
    result = {
        "title": f"{data.get('title', 'Unknown Title')} Source IP : {data.get('ip', 'Unknown')}",
        "content": data["content"],
    }
    return result
