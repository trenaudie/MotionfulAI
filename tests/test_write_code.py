# test_write_code.py
import requests
import json

def test_write_code():
    url = 'http://localhost:5000/write_code'
    headers = {'Content-Type': 'application/json'}
    payload = {
        'prompt': 'create a bouncing circle animation using motion-canvas'
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        print("Status Code:", response.status_code)
        print("Response JSON:", response.json())
    except Exception as e:
        print("Error while sending request:", e)

if __name__ == '__main__':
    test_write_code()
