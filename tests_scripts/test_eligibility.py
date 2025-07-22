import requests

url = "http://127.0.0.1:8000/api/check-eligibility/"

payload = {
    "customer_id": 1,
    "loan_amount": 50000,
    "interest_rate": 10,  # Annual interest rate in percent
    "tenure": 12          # Tenure in months
}

response = requests.post(url, json=payload)

print("Status Code:", response.status_code)
print("Response:", response.json())
