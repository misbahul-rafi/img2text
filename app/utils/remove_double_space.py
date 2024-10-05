import re
def remove_double_space(text):
    text = re.sub(r'\n{2,}', '\n', text)
    text = re.sub(r'\s{2,}', ' ', text)
    text = re.split(r'Containment\s*:|Summary\s*', text)[0]
    return text