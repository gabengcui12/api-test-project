import pytest
import requests
from config import BASE_URL

def clear_cart(api_token):
    """清空购物车"""
    headers = {"Authorization": f"Bearer {api_token}"}
    resp = requests.get(f"{BASE_URL}/api/cart", headers=headers, timeout=10)
    if resp.status_code != 200:
        return
    items = resp.json().get("items", [])
    for item in items:
        delete_url = f"{BASE_URL}/api/cart/{item.get('productId')}"
        requests.delete(delete_url, headers=headers, timeout=10)
    print("✅ 购物车已清空")

def test_add_cart_no_auth():
    """未登录加购 → 预期 401"""
    url = f"{BASE_URL}/api/cart"
    payload = {"productId": 103, "quantity": 1}
    resp = requests.post(url, json=payload, timeout=10)
    assert resp.status_code == 401
    data = resp.json()
    assert data.get("code") == 401
    assert "登录" in data.get("message", "")
    print("✅ 未登录加购返回 401")

def test_create_order_empty_cart(api_token):
    """购物车为空时下单 → 预期 400"""
    clear_cart(api_token)  # 直接清空购物车
    headers = {"Authorization": f"Bearer {api_token}"}
    url = f"{BASE_URL}/api/orders"
    resp = requests.post(url, json={}, headers=headers, timeout=10)
    assert resp.status_code == 400, f"预期 400，实际 {resp.status_code}"
    data = resp.json()
    assert data.get("code") == 400
    assert "购物车为空" in data.get("message", "")
    print("✅ 购物车为空下单返回 400")

def test_add_cart_product_not_exist(api_token):
    """商品不存在时加购 → 预期 404"""
    headers = {"Authorization": f"Bearer {api_token}"}
    url = f"{BASE_URL}/api/cart"
    payload = {"productId": 9999, "quantity": 1}
    resp = requests.post(url, json=payload, headers=headers, timeout=10)
    assert resp.status_code == 404
    data = resp.json()
    assert "不存在" in data.get("message", "")
    print("✅ 商品不存在加购返回 404")
