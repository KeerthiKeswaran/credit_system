import requests

url = "http://127.0.0.1:8000/api/create-loan/"
payload = {
    "customer_id": 1,
    "loan_amount": 100000,
    "interest_rate": 10.0,
    "tenure": 12
}

res = requests.post(url, json=payload)
print("Status Code:", res.status_code)
print("Response:", res.json())
