"""
Usage:

python memorize.py \
    [<Images directory path, default: 'images'>] \
    [<FaceKeeper API URL, default: 'http://127.0.0.1/memorize>']

This script allows to bulk recognize persons on images from directories structure:
<source directory: default current work directory>
|-- <person 1>
|   |-- <filename 1>.jpg
|   |-- <filename 2>.jpg
....
|-- <person 2>
"""

import sys
import os
import requests

directory = (len(sys.argv) > 1 and sys.argv[1]) or os.path.join(os.getcwd(), 'images')
url = (len(sys.argv) > 2 and sys.argv[2]) or 'http://127.0.0.1/recognize'

print('Root directory: ' + directory)

for person in os.scandir(directory):
    print('Person to upload: ' + person.name)
    for file in os.scandir(person.path):
        print('File to recognize: ' + file.name)
        content = {'file': (file.name, open(file.path, 'rb'), 'image/png')}
        response = requests.post(url, files=content)
        print('Response: ' + response.text)
