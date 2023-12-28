import requests
import json

# Part 1
url = "https://poetrydb.org/author,title/Shakespeare;Sonnet"

response = requests.get(url)

if response.status_code == 200:
    print("Request was successful!")
    print("Response content:")
    print(response.text)

    data = json.loads(response.text)