import re

def formatting(data_list):
    category = {}
    categories = []
    errors = []
    to_remove = ['-', '&', r'Vv', '!', '@', '#', 'Telkomsat', r'\s\s', r'\s\s\s', "Possible"]
    
    for index, data in enumerate(data_list):
        detection = re.search(r'Detection\s*:\s*([^\n]+)', data)
        ip = re.search(r'Source IP\s*:\s*([^\n]+)', data)

        detection = detection.group(1).strip() if detection else None
        ip = ip.group(1).strip() if ip else None

        if not detection or not ip:
            errors.append(f"Tidak dapat membaca file: {index + 1}")
            continue

        if detection and ip:
            # Menghapus karakter yang tidak diinginkan dari detection
            for char in to_remove:
                detection = re.sub(char, '', detection).strip()

            # Memeriksa apakah detection sudah ada di dalam list categories
            if any(category['category'] == detection for category in categories):
                print("Sudah ada")
            else:
                print(detection, "belum ada di", categories)
                categories.append({"category": detection})
                categories.append("contains": [])
                # categories.append({"content": detection})
                
                # categories.append({"ip": ip})
                # categories.append({"content": data})
    return categories
    closed_messages = []
    for detection, ips in category.items():
        if 'Web Scanner' in detection:
            firewall = 'CheckPoint'
        elif 'Web App Attack' in detection:
            firewall = 'CheckPoint'
        elif 'Sophos IPS' in detection:
            firewall = 'Sophos'
        else:
            firewall = 'Unknown'

        ip_addresses = ' '.join(ips)
        closed_messages.append(f"Sudah dilakukan blocking IP Address untuk {detection} pada firewall {firewall} dengan IP Source {ip_addresses}")

    # Create the desired output format
    result = []
    for i, content in enumerate(data_list):
        if i < len(closed_messages):  # Ensure we have a matching closed message
            result.append({
                "closed": closed_messages[i],
                "content": content.strip()  # Use original content with stripping
            })
        else:
            # Append logs without matching closed messages
            result.append({
                "closed": "Tidak ada tindakan yang diambil.",
                "content": content.strip()
            })
    return {
        "error": errors,
        "result": result  # Return the new structured result
    }