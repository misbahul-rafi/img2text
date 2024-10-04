import re

def formatting(data_list):
    category = {}
    errors = []
    content= []
    to_remove = ['-', '&', r'Vv', '!', '@', '#', 'Telkomsat', r'\s\s', r'\s\s\s', "Possible"]
    for index, data in enumerate(data_list):
        
        detection = re.search(r'Detection\s*:\s*([^\n]+)', data)
        ip = re.search(r'Source IP\s*:\s*([^\n]+)', data)
        
        detection = detection.group(1).strip() if detection else None
        ip = ip.group(1).strip() if ip else None
        
        if not detection or not ip:
            errors.append(f"Tidak dapat membaca file: {index+1}")
            continue
        
        if detection and ip:
            for char in to_remove:
                detection = re.sub(char, '', detection).strip()
            content.append(data)
            if detection in category:
                category[detection].append(ip)
            else:
                category[detection] = [ip]
                
    title_parts = []
    for detection, ips in category.items():
        title_parts.append(f"{detection} {' '.join(ips)}")
    title = " & ".join(title_parts)
    
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
    

    return {
        "title": title_parts,
        "closed": closed_messages,
        "error": errors,
        "content": content
    }
