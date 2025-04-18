import requests

url = "http://127.0.0.1:8000/ask/"
data = {"question": "What is the estimated harvest time for wheat?"}

response = requests.post(url, json=data)
print(response.json())  # Expected output: {"answer": "Estimated harvest time: XX days"}
