"""
Usage:

python memorize.py \
    [<Images directory path, default: 'images'>] \
    [<FaceKeeper API URL, default: 'http://127.0.0.1/memorize>']

This script allows to bulk load images to the FaceKeeper database from directories structure:
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
url = (len(sys.argv) > 2 and sys.argv[2]) or 'http://127.0.0.1/memorize'

print('Root directory: ' + directory)

for person in os.scandir(directory):
    print('Person to upload: ' + person.name)
    for file in os.scandir(person.path):
        print('File to memorize: ' + file.name)
        files = [
            ('files', (file.name, open(file.path, 'rb'), 'image/png'))
        ]
        response = requests.post(url, data={'person': person.name}, files=files)
        print('Response: ' + response.text)
