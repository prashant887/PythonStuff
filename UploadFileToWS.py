import requests

files = {
    'file': ('abc', open('abc.txt', 'rb'))
}

response = requests.post('http://127.0.0.1:5000/uploadfile', files=files, timeout=60)

print(('HTTP response status ' + str(response.status_code)))
