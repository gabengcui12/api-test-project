import requests
from config import BASE_URL

def test_create_order(api_token):
    headers = {"Authorization": f"Bearer {api_token}"}

    # 清空购物车（先查询再删除）
    cart_url = f"{BASE_URL}/api/cart"
    resp = requests.get(cart_url, headers=headers)
    if resp.status_code == 200:
        items = resp.json().get("items", [])
        for item in items:
            delete_url = f"{BASE_URL}/api/cart/{item.get('productId')}"
            requests.delete(delete_url, headers=headers)

    # 重新加购
    cart_payload = {"productId": 103, "quantity": 1}
    resp = requests.post(cart_url, json=cart_payload, headers=headers)
    assert resp.status_code == 200, f"加购失败: {resp.text}"
    print("✅ 前置加购成功")

    # 查询当前库存
    url = f"{BASE_URL}/api/products"
    resp = requests.get(url, headers=headers)
    products = resp.json().get("products", [])
    product = next((p for p in products if p["id"] == 103), None)
    assert product is not None
    initial_stock = product["stock"]
    print(f"📦 初始库存: {initial_stock}")

    # 创建订单
    order_url = f"{BASE_URL}/api/orders"
    resp = requests.post(order_url, json={}, headers=headers)
    assert resp.status_code == 200, f"创建订单失败: {resp.text}"
    order_data = resp.json()
    assert order_data["code"] == 0
    order_id = order_data["order"]["id"]
    print(f"✅ 订单创建成功，订单号: {order_id}")

    # 再次查询库存
    resp = requests.get(url, headers=headers)
    products = resp.json().get("products", [])
    product = next((p for p in products if p["id"] == 103), None)
    new_stock = product["stock"]
    print(f"📦 下单后库存: {new_stock}")

    assert new_stock == initial_stock - 1, f"库存扣减异常: {initial_stock} → {new_stock}"
    print(f"✅ 库存扣减验证通过: {initial_stock} → {new_stock}")
