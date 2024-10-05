import re

def formatting(data_list):
    categories = []
    errors = []
    attacks_classification = [
        {
            "attack": "Web App Attack",
            "firewall": "Check Point"
        },
        {
            "attack": "Web Scanner",
            "firewall": "Check Point"
        },
        {
            "attack": "Sophos IPS",
            "firewall": "Sophos BGR, JTN dan PTM"
        },
        {
            "attack": "Sangfor",
            "firewall": "NGAF-01"
        }
    ]
    to_remove = ['-', '&', r'Vv', '!', '@', '#', 'Telkomsat', r'\s\s', r'\s\s\s', "Possible"]
    
    for index, data in enumerate(data_list):
        detection = re.search(r'Detection\s*:\s*([^\n]+)', data)
        ip = re.search(r'Source IP\s*:\s*([^\n]+)', data)

        detection = detection.group(1).strip() if detection else None
        ip = ip.group(1).strip() if ip else None

        if not detection or not ip:
            errors.append(f"file {index + 1} can't read")
            continue

        if detection and ip:
            for char in to_remove:
                detection = re.sub(char, '', detection).strip()
                
        existing_item = next((item for item in categories if item["detection"] == detection), None)
        if existing_item:
            existing_item["ip"].append(ip)
            existing_item["content"].append(data)
        else:
            include = {
                'detection': detection,
                'ip': [ip],
                'content': [data]
            }
            categories.append(include)
            
    results = []
    for category in categories:
        detection = category["detection"]
        ip_string = " ".join(category["ip"])
        title = f"{detection} {ip_string}"
        
        closed = ''
        for item in attacks_classification:
            if detection in item["attack"]:
                closed = f"Sudah dilakukan blocking IP Source untuk {detection} pada firewall {item['firewall']} dengan detail IP {ip_string}"
        
        result = {
            "title": title,
            "closed": closed,
            "content": "\n".join(category["content"])
        }
        results.append(result)
    return {
        "error": errors,
        "results": results
    }
    return response
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