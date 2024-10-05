import re
from .remove_double_space import remove_double_space

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
        data = remove_double_space(data)

        detection_match = re.search(r'Detection\s*:\s*([^\n]+)', data)
        ip_match = re.search(r'Source IP\s*:\s*([^\n]+)', data)

        if not detection_match or not ip_match:
            errors.append(f"file {index + 1} can't read")
            continue

        detection = re.sub('|'.join(to_remove), '', detection_match.group(1)).strip()
        ip = ip_match.group(1).strip()

        existing_item = next((item for item in categories if item["detection"] == detection), None)
        if existing_item:
            existing_item["ip"].append(ip)
            existing_item["content"].append(data)
        else:
            categories.append({
                'detection': detection,
                'ip': [ip],
                'content': [data]
            })

    results = []
    for category in categories:
        title = f"{category['detection']} {' '.join(category['ip'])}"
        closed = next((
            f"Sudah dilakukan blocking IP Source untuk {category['detection']} pada firewall {item['firewall']} dengan detail IP {' '.join(category['ip'])}"
            for item in attacks_classification if category['detection'] in item["attack"]
        ), '')

        results.append({
            "title": title,
            "closed": closed,
            "content": "\n".join(category["content"])
        })

    return {
        "error": errors,
        "results": results
    }