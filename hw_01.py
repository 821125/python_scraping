import requests
import json
from pprint import pprint

# 1. View the documentation for the GitHub API, understand how to display a list of repositories
# for a specific user, save the JSON output in the *.json.

service = 'https://api.github.com'
user='821125'
req = requests.get(f'{service}/users/{user}/repos')

with open('data_git.json', 'w') as f:
    json.dump(req.json(), f)
    
for i in req.json():
    print(i['name'])
    
# 2. To watch the list of open APIs. Finds among them any, that have needed authorization (any type).
# Perform queries to it after the authorization. The server's request should be writing on file.

service = 'https://currate.ru/api'
get = 'rates&pairs'
pairs = 'USDRUB,EURRUB'
key = '09397da287c95a555909a5a544b80af3'

req = requests.get(f'{service}/?get={get}={pairs}&key={key}')

with open('data_currency.json', 'w') as f:
    json.dump(req.json(), f)
    
j_data = req.json()
pprint(j_data)

for i in (j_data.get('data')):
    print(i, j_data.get('data').get(i))
