import requests
from config import BASE_URL, LOGIN_USER, LOGIN_PASS

def test_login_success():
    url = f"{BASE_URL}/api/login"
    payload = {"username": LOGIN_USER, "password": LOGIN_PASS}
    resp = requests.post(url, json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    assert "token" in data
    print(f"✅ 登录成功，Token: {data['token'][:20]}...")
