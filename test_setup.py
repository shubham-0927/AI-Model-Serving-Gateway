#!/usr/bin/env python3
"""
Test Setup Script - Creates test user and API key
Runs once before starting load tests
"""

import requests
import sys
import time
from datetime import datetime

BASE_URL = "http://localhost"
TEST_USER_EMAIL = "testuser@loadtest.com"
TEST_USER_PASSWORD = "TestPass123!@#"

def setup_test_environment():
    """Create test user and generate API key"""
    print(f"[{datetime.now().isoformat()}] Setting up test environment...")
    
    max_retries = 5
    for attempt in range(max_retries):
        try:
            # Check API health
            health = requests.get(f"{BASE_URL}/health", timeout=5)
            if health.status_code == 200:
                print(f"✓ API is healthy")
                break
        except requests.exceptions.ConnectionError:
            if attempt == max_retries - 1:
                print(f"✗ Failed to connect to API after {max_retries} attempts")
                sys.exit(1)
            print(f"Retrying to connect... (attempt {attempt + 1}/{max_retries})")
            time.sleep(5)
    
    try:
        # Register test user
        print(f"Registering test user: {TEST_USER_EMAIL}")
        register_response = requests.post(
            f"{BASE_URL}/auth/register",
            json={
                "email": TEST_USER_EMAIL,
                "password": TEST_USER_PASSWORD
            },
            timeout=10
        )
        
        if register_response.status_code == 200:
            print(f"✓ User created: {register_response.json()}")
        else:
            print(f"⚠ User registration response: {register_response.status_code} - {register_response.text}")
        
        # Login to get token
        print(f"Logging in...")
        login_response = requests.post(
            f"{BASE_URL}/auth/login",
            json={
                "email": TEST_USER_EMAIL,
                "password": TEST_USER_PASSWORD
            },
            timeout=10
        )
        
        if login_response.status_code != 200:
            print(f"✗ Login failed: {login_response.status_code}")
            sys.exit(1)
        
        access_token = login_response.json().get("access_token")
        print(f"✓ Got access token")
        
        # Generate API key
        print(f"Generating API key...")
        key_response = requests.post(
            f"{BASE_URL}/keys/",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10
        )
        
        if key_response.status_code != 200:
            print(f"✗ API key generation failed: {key_response.status_code}")
            sys.exit(1)
        
        api_key = key_response.json().get("api_key")
        print(f"✓ Generated API key: {api_key[:20]}...")
        
        # Save to file
        with open("test_api_key.txt", "w") as f:
            f.write(api_key)
        
        print(f"✓ Test environment setup complete!")
        print(f"  API Key saved to: test_api_key.txt")
        return api_key
        
    except Exception as e:
        print(f"✗ Error during setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    api_key = setup_test_environment()
