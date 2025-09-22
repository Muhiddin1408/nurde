import base64

import requests
import json


def add_card(card_number, card_expire, card_id, merchant_id):
    if not all([card_number, card_expire, card_id]):
        raise ValueError("All parameters are required")
    credentials = f"{merchant_id}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/json'
    }

    url = 'https://checkout.paycom.uz/api'
    data = {
        "jsonrpc": "2.0",
        "id": str(card_id),
        "method": "cards.create",
        "params": {
            "card": {
                "number": str(card_number),
                "expire": str(card_expire)
            },
            "save": False
        }
    }
    payload = json.dumps(data)
    print(payload)

    try:
        r = requests.post(url, json=data, timeout=30, headers=headers)
        print(r.text)
        r.raise_for_status()  # Raises exception for 4xx/5xx status codes
        return r.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {e}")
    except json.JSONDecodeError:
        raise Exception("Invalid JSON response from API")


