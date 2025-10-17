#!/usr/bin/env python3
"""
Test script for DeFi Assistant new features
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8080"

def test_endpoint(method, endpoint, data=None, params=None):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, params=params, timeout=10)
        else:
            response = requests.post(url, json=data, timeout=10)
        
        print(f"\n🔍 Testing {method} {endpoint}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: {result.get('success', 'N/A')}")
            if 'data' in result:
                print(f"📊 Data keys: {list(result['data'].keys())}")
            if 'message' in result:
                print(f"💬 Message preview: {result['message'][:100]}...")
        else:
            print(f"❌ Error: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def main():
    print("🚀 Testing DeFi Assistant New Features")
    print("=" * 50)
    
    # Test Sentient API
    test_endpoint("GET", "/api/sentient/info")
    
    test_endpoint("POST", "/api/sentient/query", {
        "query": "What are current gas prices?",
        "context": {}
    })
    
    # Test Portfolio Analysis
    test_endpoint("GET", "/api/portfolio/analyze", params={
        "wallet": "0x1234567890123456789012345678901234567890"
    })
    
    test_endpoint("POST", "/api/portfolio/analyze", {
        "wallet_address": "0x1234567890123456789012345678901234567890"
    })
    
    # Test MEV Protection
    test_endpoint("GET", "/api/mev/status")
    
    test_endpoint("GET", "/api/mev/alerts", params={
        "wallet": "0x1234567890123456789012345678901234567890"
    })
    
    test_endpoint("POST", "/api/mev/check", {
        "transaction_data": {
            "value": 15.5,
            "function_name": "swapExactTokensForTokens",
            "protocol": "uniswap",
            "slippage_tolerance": 3.0,
            "gas_price": 45
        }
    })
    
    print("\n🎉 Testing completed!")
    print("\n📱 You can also test via web interface:")
    print(f"   • Main app: {BASE_URL}")
    print(f"   • AI Chat: {BASE_URL}/chat")
    print(f"   • Gas Prices: {BASE_URL}/gas-prices")
    print(f"   • Market Data: {BASE_URL}/market-data")

if __name__ == "__main__":
    main()
