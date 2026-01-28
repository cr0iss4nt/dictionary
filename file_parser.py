from striprtf.striprtf import rtf_to_text



def parse_txt(filename):
    with open(filename, 'r') as f:
        content = f.read()
        return content

def parse_rtf(filename):
    with open(filename) as f:
        content = f.read()
        text = rtf_to_text(content)
        return text