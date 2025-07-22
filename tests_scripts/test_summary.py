import requests

res = requests.get("http://127.0.0.1:8000/api/loan-summary/1/")
print("Status Code:", res.status_code)
print("Response:", res.json())
