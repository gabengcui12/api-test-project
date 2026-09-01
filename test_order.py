import requests
from config import BASE_URL, PRODUCT_ID, QUANTITY

def ensure_cart_not_empty(api_token):
    """确保购物车至少有一件商品"""
    url = f"{BASE_URL}/api/cart"
    headers = {"Authorization": f"Bearer {api_token}"}
    payload = {"productId": PRODUCT_ID, "quantity": QUANTITY}
    resp = requests.post(url, json=payload, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        if data.get("code") == 0:
            print(f"✅ 前置加购成功（商品 {PRODUCT_ID}）")
            return
    print(f"⚠️ 加购失败: {resp.json()}")

def test_create_order(api_token):
    ensure_cart_not_empty(api_token)
    url = f"{BASE_URL}/api/orders"
    headers = {"Authorization": f"Bearer {api_token}"}
    resp = requests.post(url, json={}, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    print(f"创建订单响应: {data}")
    assert data["code"] == 0
    assert "order" in data
    order_id = data["order"]["id"]
    assert order_id is not None
    print(f"✅ 订单创建成功，订单号: {order_id}")

def test_get_order_detail(api_token):
    ensure_cart_not_empty(api_token)
    url = f"{BASE_URL}/api/orders"
    headers = {"Authorization": f"Bearer {api_token}"}
    resp = requests.post(url, json={}, headers=headers)
    data = resp.json()
    if data.get("code") != 0:
        print(f"❌ 创建订单失败: {data}")
        assert False, f"创建订单失败: {data}"
    order_id = data["order"]["id"]

    detail_url = f"{BASE_URL}/api/orders/{order_id}"
    resp = requests.get(detail_url, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    assert data["order"]["id"] == order_id
    assert data["order"]["status"] == "pending"
    print(f"✅ 订单详情查询成功，状态: {data['order']['status']}")
