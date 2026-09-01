import pytest
import requests
from config import BASE_URL, LOGIN_USER, LOGIN_PASS

@pytest.fixture(scope="session")
def api_token():
    url = f"{BASE_URL}/api/login"
    payload = {"username": LOGIN_USER, "password": LOGIN_PASS}
    resp = requests.post(url, json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("code") == 0
    assert "token" in data
    return data["token"]
