import pytest
import requests
from config import BASE_URL

def reset_environment(api_token):
    """调用重置接口，恢复环境到初始状态"""
    headers = {"Authorization": f"Bearer {api_token}"}
    url = f"{BASE_URL}/api/admin/reset"
    try:
        resp = requests.post(url, json={}, headers=headers, timeout=10)
        if resp.status_code == 200:
            print("✅ 环境重置成功")
        else:
            print(f"⚠️ 环境重置失败: {resp.status_code}")
    except requests.exceptions.Timeout:
        print("⚠️ 重置请求超时，跳过")
    except Exception as e:
        print(f"⚠️ 环境重置异常: {e}")

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
    reset_environment(api_token)
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
