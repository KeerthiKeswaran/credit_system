import requests

url = "http://127.0.0.1:8000/api/register/"
payload = {
    "first_name": "Keerthi",
    "last_name": "Keswaran",
    "age": 22,
    "monthly_income": 50000,
    "phone_number": "9876543210"
}

response = requests.post(url, json=payload)

print("Status Code:", response.status_code)
print("Response:", response.json())
