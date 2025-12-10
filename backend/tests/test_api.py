"""
Test Backend API - Quick Verification Script
"""

import requests
import json
from typing import Dict, Any


BASE_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint"""
    print("1. Testing Health Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"   ✓ Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return True
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False


def test_collection_stats():
    """Test collection stats endpoint"""
    print("\n2. Testing Collection Stats...")
    try:
        response = requests.get(f"{BASE_URL}/api/admin/collection/stats")
        data = response.json()
        print(f"   ✓ Status: {response.status_code}")
        print(f"   Vectors: {data.get('data', {}).get('vectors_count', 0)}")
        return True
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False


def test_chat(question: str = "What is RAG?"):
    """Test chat endpoint"""
    print(f"\n3. Testing Chat Endpoint...")
    print(f"   Question: {question}")
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json={"question": question, "top_k": 3}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Status: {response.status_code}")
            print(f"   Answer: {data['answer'][:100]}...")
            print(f"   Sources: {len(data['sources'])} found")
            for src in data['sources']:
                print(f"     - {src['page_title']} (score: {src['relevance_score']:.2f})")
            return True
        else:
            print(f"   ✗ Status: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False


def test_chat_stream(question: str = "Explain vector embeddings"):
    """Test streaming chat endpoint"""
    print(f"\n4. Testing Streaming Chat...")
    print(f"   Question: {question}")
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat/stream",
            json={"question": question, "top_k": 3},
            stream=True
        )
        
        print(f"   ✓ Streaming response:")
        print("   ", end="")
        
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    data = json.loads(line_str[6:])
                    if data.get('type') == 'token':
                        print(data['token'], end="", flush=True)
                    elif data.get('type') == 'sources':
                        print(f"\n\n   Sources: {len(data['sources'])} found")
                    elif data.get('type') == 'done':
                        print("\n   ✓ Stream complete")
        
        return True
        
    except Exception as e:
        print(f"\n   ✗ Error: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("Backend API Test Suite")
    print("="*60)
    
    # Check if server is running
    try:
        requests.get(BASE_URL, timeout=2)
    except:
        print("\n✗ ERROR: Backend server is not running!")
        print("  Start it with: cd backend && uvicorn app.main:app --reload")
        return
    
    print("\n✓ Server is running\n")
    
    # Run tests
    results = []
    results.append(("Health Check", test_health()))
    results.append(("Collection Stats", test_collection_stats()))
    results.append(("Chat Endpoint", test_chat()))
    results.append(("Streaming Chat", test_chat_stream()))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All tests passed! Backend is working correctly.")
    else:
        print(f"\n⚠ {total - passed} test(s) failed. Check the errors above.")


if __name__ == "__main__":
    run_all_tests()
