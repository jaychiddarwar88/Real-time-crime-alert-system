import requests


data = {
    'query': open('query.rq').read(),
}

response = requests.post('http://localhost:3030/ds/query', data=data)

print(response.text)