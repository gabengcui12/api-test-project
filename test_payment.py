import requests
from config import BASE_URL

def ensure_cart_not_empty(api_token):
    url = f"{BASE_URL}/api/cart"
    headers = {"Authorization": f"Bearer {api_token}"}
    payload = {"productId": 103, "quantity": 1}
    resp = requests.post(url, json=payload, headers=headers)
    if resp.status_code == 200 and resp.json().get("code") == 0:
        print("✅ 前置加购成功")
    else:
        print("⚠️ 加购失败:", resp.json())

def test_pay_order(api_token):
    ensure_cart_not_empty(api_token)

    # 创建订单
    create_url = f"{BASE_URL}/api/orders"
    headers = {"Authorization": f"Bearer {api_token}"}
    resp = requests.post(create_url, json={}, headers=headers)
    data = resp.json()
    assert data["code"] == 0
    order_id = data["order"]["id"]
    print(f"✅ 订单创建成功，订单号: {order_id}")

    # 支付订单
    pay_url = f"{BASE_URL}/api/orders/{order_id}/pay"
    resp = requests.post(pay_url, json={}, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    assert data["order"]["status"] == "paid"
    print(f"✅ 支付成功，订单状态: {data['order']['status']}")

    # 再次查询订单详情，确认状态已变
    detail_url = f"{BASE_URL}/api/orders/{order_id}"
    resp = requests.get(detail_url, headers=headers)
    data = resp.json()
    assert data["order"]["status"] == "paid"
    print(f"✅ 支付后查订单，状态: {data['order']['status']}")
