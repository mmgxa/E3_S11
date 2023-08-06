import requests

url = "http://127.0.0.1:80/clip?text=cat&text=dog"

payload = {}
files=[
  ('image',('cat.jpg',open('cat.jpg','rb'),'image/jpeg'))
]
headers = {}

response = requests.request("GET", url, headers=headers, data=payload, files=files)

print(response.text)
