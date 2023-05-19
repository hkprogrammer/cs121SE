import os
import json
from bs4 import BeautifulSoup
from unicodedata import normalize
from tqdm import tqdm

#https://stackoverflow.com/questions/33263669/how-to-remove-nonascii-characters-in-python

#TODO, implemenet read in zip.

def extract_text_from_json_files(filename):

    file_list = []
    
    # for dirpath, dirnames, filenames in tqdm(os.walk(root_dir)):
    #     for filename in filenames:
    #         if filename.endswith('.json'):
    #             file_list.append(os.path.join(dirpath, filename))
    # print("===============Extracting Texts=================")
    # for json_path in tqdm(file_list):
    try:
        with open(filename) as f:
            data = json.load(f)
        html_content = data['content']
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text()
        output_filename = os.path.splitext(filename)[0] + '.txt'
        # print(output_filename)
        normalize('NFKD', text).encode('ASCII', 'ignore')
        # output_filename = html_url[8:-1] + '.txt'
        return text
    except Exception as e:
        print("Exception happened during extract: ",e )
    return ""
    # print(text)

    