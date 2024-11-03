import requests

if __name__ == '__main__':
    __main__()

class SourceGetter





url = "https://www.bible.com/es/bible/103/PSA.1.NBLA"

response = requests.get(url)

if response.status_code == 200:
    data
    print(response.text)
else:
    print("Failed to retrieve the page. Status code:", response.status_code)