import requests

payload = {
    "emis_paid_on_time": 6
}

res = requests.post("http://127.0.0.1:8000/api/update-loan/1/", json=payload)
print("Status Code:", res.status_code)
print("Response:", res.json())
