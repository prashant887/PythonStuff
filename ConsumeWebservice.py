import requests
import json

countries = ['india', 'italy', 'spain', 'usa', 'uganda']
url = 'http://127.0.0.1:5000/corona/'

for cntry in countries:
    cntry_url = url + cntry
    r = requests.get(cntry_url)
    print(cntry)
    #data = json.loads(r.json())
    print(json.dumps(r.json(), indent=4, sort_keys=True))
