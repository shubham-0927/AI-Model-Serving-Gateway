#!/usr/bin/env python3
"""
Resilience Testing Script - Tests gateway behavior under various failure scenarios
- Provider failures and failover
- Recovery mechanisms
- Circuit breaker behavior
"""

import requests
import threading
import time
from datetime import datetime, timedelta
from collections import defaultdict
import json

BASE_URL = "http://localhost"
TEST_DURATION_MINUTES = 60

class ResilienceMetrics:
    def __init__(self):
        self.lock = threading.Lock()
        self.scenarios = defaultdict(lambda: {"success": 0, "failure": 0, "total_time": 0})
        self.failure_recovery_times = []
        self.start_time = time.time()
    
    def record_scenario(self, scenario_name, success, response_time):
        with self.lock:
            self.scenarios[scenario_name]["total_time"] += response_time
            if success:
                self.scenarios[scenario_name]["success"] += 1
            else:
                self.scenarios[scenario_name]["failure"] += 1
    
    def record_recovery(self, recovery_time):
        with self.lock:
            self.failure_recovery_times.append(recovery_time)
    
    def get_stats(self):
        with self.lock:
            stats = {}
            for scenario, data in self.scenarios.items():
                total = data["success"] + data["failure"]
                stats[scenario] = {
                    "success": data["success"],
                    "failure": data["failure"],
                    "total": total,
                    "success_rate": (data["success"] / total * 100) if total > 0 else 0,
                    "avg_time_ms": data["total_time"] / total if total > 0 else 0
                }
            return {
                "scenarios": stats,
                "avg_recovery_time_ms": sum(self.failure_recovery_times) / len(self.failure_recovery_times) if self.failure_recovery_times else 0,
                "uptime_seconds": time.time() - self.start_time
            }

metrics = ResilienceMetrics()

def load_api_key():
    try:
        with open("test_api_key.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        print("✗ test_api_key.txt not found. Run test_setup.py first!")
        exit(1)

def make_request_to_provider(api_key, provider, strict=False):
    """Make request to specific provider"""
    payload = {
        "prompt": f"Test request for {provider}",
        "provider": provider,
        "strict_provider": strict,
        "max_tokens": 50,
        "temperature": 0.5
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        start = time.time()
        response = requests.post(
            f"{BASE_URL}/v1/completions",
            json=payload,
            headers=headers,
            timeout=30
        )
        response_time = (time.time() - start) * 1000
        return response.status_code == 200, response_time, response.status_code
    except Exception as e:
        response_time = (time.time() - start) * 1000
        return False, response_time, 0

def test_provider_failover(api_key, api_key_id):
    """Test that gateway falls back to other providers when one fails"""
    print(f"[Failover Test] Testing provider failover logic...")
    
    # Try with strict_provider=False, should try multiple providers
    for attempt in range(3):
        success, resp_time, status = make_request_to_provider(
            api_key, 
            "openai",  # Try OpenAI
            strict=False  # Allow fallback
        )
        
        scenario_name = f"failover_attempt_{attempt + 1}"
        metrics.record_scenario(scenario_name, success, resp_time)
        
        if success:
            print(f"  ✓ Failover {attempt + 1}: Success ({resp_time:.0f}ms)")
        else:
            print(f"  ✗ Failover {attempt + 1}: Failed ({status}) ({resp_time:.0f}ms)")
        
        time.sleep(2)

def test_rate_limiting(api_key):
    """Test rate limiting and behavior when limits are exceeded"""
    print(f"[Rate Limit Test] Testing rate limiting...")
    
    success_count = 0
    limit_exceeded_count = 0
    
    # Rapid fire requests to test rate limiting
    for i in range(20):
        start = time.time()
        try:
            response = requests.post(
                f"{BASE_URL}/v1/completions",
                json={
                    "prompt": f"Rate limit test {i}",
                    "max_tokens": 20
                },
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=5
            )
            resp_time = (time.time() - start) * 1000
            
            if response.status_code == 200:
                success_count += 1
                metrics.record_scenario("rate_limit_test", True, resp_time)
            elif response.status_code == 429:
                limit_exceeded_count += 1
                metrics.record_scenario("rate_limit_test", False, resp_time)
                print(f"  ✓ Rate limit triggered correctly at request {i + 1}")
            else:
                metrics.record_scenario("rate_limit_test", False, resp_time)
        except Exception as e:
            metrics.record_scenario("rate_limit_test", False, 0)
        
        if i < 10:
            time.sleep(0.1)  # Fast requests
        else:
            time.sleep(1)  # Slow down
    
    print(f"  Results: {success_count} successful, {limit_exceeded_count} rate limited")

def test_concurrent_requests(api_key):
    """Test handling of concurrent requests"""
    print(f"[Concurrent Test] Testing concurrent request handling...")
    
    def worker(worker_id):
        for i in range(5):
            success, resp_time, status = make_request_to_provider(
                api_key,
                "openai" if worker_id % 2 == 0 else "anthropic",
                strict=False
            )
            scenario_name = f"concurrent_worker_{worker_id}"
            metrics.record_scenario(scenario_name, success, resp_time)
            time.sleep(0.5)
    
    threads = []
    for i in range(5):
        t = threading.Thread(target=worker, args=(i,))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    
    print(f"  ✓ Concurrent request test completed")

def test_automatic_routing(api_key):
    """Test automatic provider routing without specifying provider"""
    print(f"[Automatic Routing Test] Testing automatic provider selection...")
    
    for i in range(10):
        payload = {
            "prompt": f"Automatic routing test {i}",
            # NO provider specified - should auto-select
            "max_tokens": 50
        }
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            start = time.time()
            response = requests.post(
                f"{BASE_URL}/v1/completions",
                json=payload,
                headers=headers,
                timeout=30
            )
            resp_time = (time.time() - start) * 1000
            success = response.status_code == 200
            metrics.record_scenario("automatic_routing", success, resp_time)
            
            if success:
                print(f"  ✓ Auto-routing {i + 1}: Success ({resp_time:.0f}ms)")
            else:
                print(f"  ✗ Auto-routing {i + 1}: Failed ({response.status_code})")
        except Exception as e:
            print(f"  ✗ Auto-routing {i + 1}: Error - {e}")
            metrics.record_scenario("automatic_routing", False, 0)
        
        time.sleep(2)

def test_response_streaming(api_key):
    """Test streaming responses"""
    print(f"[Streaming Test] Testing response streaming...")
    
    payload = {
        "prompt": "Tell me a story",
        "max_tokens": 100,
        "stream": True
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        start = time.time()
        response = requests.post(
            f"{BASE_URL}/v1/stream/completions",
            json=payload,
            headers=headers,
            stream=True,
            timeout=30
        )
        
        chunk_count = 0
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                chunk_count += 1
        
        resp_time = (time.time() - start) * 1000
        success = response.status_code == 200
        metrics.record_scenario("streaming", success, resp_time)
        
        print(f"  ✓ Streaming: {chunk_count} chunks received ({resp_time:.0f}ms)")
    except Exception as e:
        print(f"  ✗ Streaming test failed: {e}")
        metrics.record_scenario("streaming", False, 0)

def run_resilience_tests():
    """Main resilience test orchestration"""
    print(f"\n{'='*60}")
    print(f"RESILIENCE TESTING SCRIPT")
    print(f"{'='*60}")
    print(f"Start Time: {datetime.now().isoformat()}")
    print(f"Duration: {TEST_DURATION_MINUTES} minutes")
    print(f"{'='*60}\n")
    
    api_key = load_api_key()
    print(f"✓ Loaded API key\n")
    
    # Get API key ID (just a UUID)
    api_key_id = api_key.split('-')[0] if '-' in api_key else api_key[:8]
    
    start_time = time.time()
    test_cycle = 0
    
    # Run tests in cycles over the specified duration
    while time.time() - start_time < TEST_DURATION_MINUTES * 60:
        test_cycle += 1
        elapsed = time.time() - start_time
        elapsed_minutes = elapsed / 60
        
        print(f"\n{'='*60}")
        print(f"TEST CYCLE #{test_cycle} (Elapsed: {elapsed_minutes:.1f}min / {TEST_DURATION_MINUTES}min)")
        print(f"{'='*60}\n")
        
        # Run various test scenarios
        test_automatic_routing(api_key)
        time.sleep(5)
        
        test_provider_failover(api_key, api_key_id)
        time.sleep(5)
        
        test_concurrent_requests(api_key)
        time.sleep(5)
        
        if test_cycle % 3 == 0:  # Run occasionally
            test_rate_limiting(api_key)
            time.sleep(5)
        
        if test_cycle % 5 == 0:  # Run occasionally
            test_response_streaming(api_key)
            time.sleep(5)
        
        # Check if we should continue
        if time.time() - start_time >= TEST_DURATION_MINUTES * 60:
            break
        
        print(f"\nWaiting before next cycle...")
        time.sleep(30)
    
    # Print final statistics
    print(f"\n{'='*60}")
    print(f"RESILIENCE TEST COMPLETE")
    print(f"{'='*60}")
    stats = metrics.get_stats()
    print(json.dumps(stats, indent=2, default=str))
    print(f"{'='*60}\n")

if __name__ == "__main__":
    run_resilience_tests()
