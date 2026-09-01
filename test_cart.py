import requests
from config import BASE_URL, PRODUCT_ID, QUANTITY

def test_add_to_cart(api_token):
    url = f"{BASE_URL}/api/cart"
    headers = {"Authorization": f"Bearer {api_token}"}
    payload = {"productId": PRODUCT_ID, "quantity": QUANTITY}
    resp = requests.post(url, json=payload, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    assert "items" in data
    print(f"✅ 加购成功，商品ID: {PRODUCT_ID}")

def test_get_cart(api_token):
    url = f"{BASE_URL}/api/cart"
    headers = {"Authorization": f"Bearer {api_token}"}
    resp = requests.get(url, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    assert "items" in data
    print(f"✅ 购物车共有 {len(data['items'])} 件商品")
