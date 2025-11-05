#!/usr/bin/env python3
"""
Simple script to test if the backend is running and accessible.
Run this to verify your backend is working correctly.
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_backend():
    print("Testing Electricity Supply Logger Backend...")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Testing health check endpoint (GET /)...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✓ Health check passed")
            print(f"  Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"✗ Health check failed with status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to backend!")
        print("  Make sure the backend is running:")
        print("  cd backend")
        print("  python app.py")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
    
    # Test 2: API info
    print("\n2. Testing API info endpoint (GET /api)...")
    try:
        response = requests.get(f"{BASE_URL}/api")
        if response.status_code == 200:
            print("✓ API info endpoint works")
            print(f"  Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"✗ API info failed with status {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 3: Register endpoint
    print("\n3. Testing register endpoint (POST /api/register)...")
    try:
        test_user = {
            "username": f"testuser_{hash(str(__import__('time').time()))}",
            "password": "testpass123"
        }
        response = requests.post(
            f"{BASE_URL}/api/register",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 201:
            print("✓ Register endpoint works")
            data = response.json()
            print(f"  Registered user: {data.get('username')}")
            print(f"  Token received: {bool(data.get('token'))}")
        else:
            print(f"✗ Register failed with status {response.status_code}")
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "=" * 50)
    print("Backend test completed!")
    print("\nIf all tests passed, your backend is working correctly.")
    return True

if __name__ == "__main__":
    test_backend()

