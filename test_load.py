#!/usr/bin/env python3
"""
Load Testing Script - Simulates normal user load
Generates steady request traffic to measure performance and resilience
"""

import requests
import threading
import time
import statistics
from datetime import datetime
from collections import defaultdict
import json

BASE_URL = "http://localhost"
NUM_THREADS = 10
REQUESTS_PER_THREAD = 5  # per minute, adjusted for 1-hour test
TEST_DURATION_MINUTES = 60

# Metrics collection
class MetricsCollector:
    def __init__(self):
        self.lock = threading.Lock()
        self.response_times = []
        self.request_counts = defaultdict(int)
        self.error_counts = defaultdict(int)
        self.status_codes = defaultdict(int)
        self.start_time = time.time()
    
    def record_request(self, status_code, response_time, provider=None):
        with self.lock:
            self.response_times.append(response_time)
            self.request_counts["total"] += 1
            self.status_codes[status_code] += 1
            if provider:
                self.request_counts[provider] += 1
            if status_code >= 400:
                self.error_counts[status_code] += 1
    
    def record_error(self, error_type):
        with self.lock:
            self.error_counts[error_type] += 1
            self.request_counts["failed"] += 1
    
    def get_stats(self):
        with self.lock:
            if not self.response_times:
                return {}
            return {
                "total_requests": self.request_counts["total"],
                "failed_requests": self.request_counts["failed"],
                "avg_response_time_ms": statistics.mean(self.response_times),
                "min_response_time_ms": min(self.response_times),
                "max_response_time_ms": max(self.response_times),
                "median_response_time_ms": statistics.median(self.response_times),
                "p95_response_time_ms": statistics.quantiles(self.response_times, n=20)[18] if len(self.response_times) > 1 else 0,
                "p99_response_time_ms": statistics.quantiles(self.response_times, n=100)[98] if len(self.response_times) > 1 else 0,
                "status_codes": dict(self.status_codes),
                "error_counts": dict(self.error_counts),
                "uptime_seconds": time.time() - self.start_time
            }

metrics = MetricsCollector()

def load_api_key():
    """Load API key from file created by test_setup.py"""
    try:
        with open("test_api_key.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        print("✗ test_api_key.txt not found. Run test_setup.py first!")
        exit(1)

test_prompts = [
    "What is machine learning?",
    "Explain quantum computing",
    "How does artificial intelligence work?",
    "What is the future of technology?",
    "Explain neural networks",
    "What is cloud computing?",
    "How does blockchain work?",
    "Explain cybersecurity",
    "What is data science?",
    "How does the internet work?",
]

providers = ["openai", "anthropic", None]  # None = automatic routing

def make_request(api_key, request_id):
    """Make a single request to the gateway"""
    import random
    
    provider = random.choice(providers)
    prompt = random.choice(test_prompts)
    
    payload = {
        "prompt": prompt,
        "max_tokens": 100,
        "temperature": 0.7,
        "strict_provider": False
    }
    
    if provider:
        payload["provider"] = provider
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-Request-ID": request_id
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/v1/completions",
            json=payload,
            headers=headers,
            timeout=30
        )
        response_time = (time.time() - start_time) * 1000  # ms
        
        metrics.record_request(response.status_code, response_time, provider)
        
        return {
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "response_time_ms": response_time,
            "provider": provider
        }
    except requests.exceptions.Timeout:
        metrics.record_error("timeout")
        return {"success": False, "error": "timeout"}
    except requests.exceptions.ConnectionError:
        metrics.record_error("connection_error")
        return {"success": False, "error": "connection_error"}
    except Exception as e:
        metrics.record_error(str(type(e).__name__))
        return {"success": False, "error": str(e)}

def worker_thread(api_key, thread_id, duration_seconds):
    """Worker thread that sends requests continuously"""
    print(f"[Thread {thread_id}] Starting load test")
    start_time = time.time()
    request_count = 0
    
    while time.time() - start_time < duration_seconds:
        try:
            request_id = f"load-test-{thread_id}-{request_count}"
            result = make_request(api_key, request_id)
            request_count += 1
            
            # Log occasionally
            if request_count % 20 == 0:
                elapsed = time.time() - start_time
                print(f"[Thread {thread_id}] Requests: {request_count}, "
                      f"Elapsed: {elapsed:.1f}s, "
                      f"Success: {result['success']}")
            
            # Request rate: ~5 per minute (12 seconds between requests)
            time.sleep(12)
        except KeyboardInterrupt:
            break
    
    print(f"[Thread {thread_id}] Completed - {request_count} requests")

def print_stats_periodically(interval_seconds):
    """Print statistics every N seconds"""
    while True:
        time.sleep(interval_seconds)
        stats = metrics.get_stats()
        if stats:
            print(f"\n{'='*60}")
            print(f"[{datetime.now().isoformat()}] METRICS SNAPSHOT")
            print(f"{'='*60}")
            print(f"Total Requests: {stats.get('total_requests', 0)}")
            print(f"Failed Requests: {stats.get('failed_requests', 0)}")
            print(f"Avg Response Time: {stats.get('avg_response_time_ms', 0):.2f} ms")
            print(f"P95 Response Time: {stats.get('p95_response_time_ms', 0):.2f} ms")
            print(f"P99 Response Time: {stats.get('p99_response_time_ms', 0):.2f} ms")
            print(f"Min/Max: {stats.get('min_response_time_ms', 0):.0f} / {stats.get('max_response_time_ms', 0):.0f} ms")
            print(f"Status Codes: {stats.get('status_codes', {})}")
            print(f"Uptime: {stats.get('uptime_seconds', 0):.1f}s")
            print(f"{'='*60}\n")

def run_load_test():
    """Main load test orchestration"""
    print(f"{'='*60}")
    print(f"LOAD TESTING SCRIPT")
    print(f"{'='*60}")
    print(f"Start Time: {datetime.now().isoformat()}")
    print(f"Duration: {TEST_DURATION_MINUTES} minutes")
    print(f"Num Threads: {NUM_THREADS}")
    print(f"Requests per thread per minute: {REQUESTS_PER_THREAD}")
    print(f"{'='*60}\n")
    
    api_key = load_api_key()
    print(f"✓ Loaded API key\n")
    
    # Start metrics printer thread
    stats_thread = threading.Thread(
        target=print_stats_periodically,
        args=(60,),  # Print stats every 60 seconds
        daemon=True
    )
    stats_thread.start()
    
    # Start worker threads
    threads = []
    duration_seconds = TEST_DURATION_MINUTES * 60
    
    for i in range(NUM_THREADS):
        t = threading.Thread(
            target=worker_thread,
            args=(api_key, i, duration_seconds)
        )
        t.start()
        threads.append(t)
        time.sleep(2)  # Stagger thread starts
    
    # Wait for all threads
    for t in threads:
        t.join()
    
    # Print final stats
    print(f"\n{'='*60}")
    print(f"LOAD TEST COMPLETE")
    print(f"{'='*60}")
    stats = metrics.get_stats()
    print(json.dumps(stats, indent=2, default=str))
    print(f"{'='*60}\n")

if __name__ == "__main__":
    run_load_test()
