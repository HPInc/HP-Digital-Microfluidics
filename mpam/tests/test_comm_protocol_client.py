from __future__ import annotations
import requests

endpoint = "http://127.0.0.1:8087"

r = requests.post(f"{endpoint}/message", json={"message": "This is the message"})
print(f"Got back: {r}")