import requests

customer_id = 1
res = requests.get(f"http://127.0.0.1:8000/api/loans/{customer_id}/")
print("Status Code:", res.status_code)
print("Response:", res.json())
