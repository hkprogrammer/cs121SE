import os
import json
from bs4 import BeautifulSoup

def extract_text_from_json_files(root_dir):
    file_list = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.json'):
                file_list.append(os.path.join(dirpath, filename))
    for json_path in file_list:
        with open(json_path) as f:
            data = json.load(f)
        html_content = data['content']
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text()
        output_filename = os.path.splitext(json_path)[0] + '.txt'
        with open(output_filename, 'w') as f:
            f.write(text)
    