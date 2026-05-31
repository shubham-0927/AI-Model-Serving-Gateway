#!/usr/bin/env python3
"""
Stress Testing Script - Tests gateway under high load conditions
- Burst traffic patterns
- Sustained high load
- Resource exhaustion scenarios
- Recovery after stress
"""

import requests
import threading
import time
from datetime import datetime
from collections import defaultdict
import json
import random

BASE_URL = "http://localhost"
TEST_DURATION_MINUTES = 60

class StressMetrics:
    def __init__(self):
        self.lock = threading.Lock()
        self.requests = []
        self.errors = defaultdict(int)
        self.phase_stats = {}
        self.start_time = time.time()
    
    def record_request(self, response_time, status_code, phase):
        with self.lock:
            self.requests.append({
                "time": time.time() - self.start_time,
                "response_time": response_time,
                "status_code": status_code,
                "phase": phase
            })
            if status_code >= 400:
                self.errors[status_code] += 1
    
    def get_stats(self):
        with self.lock:
            stats = {
                "total_requests": len(self.requests),
                "start_time": self.start_time,
                "errors": dict(self.errors),
                "uptime_seconds": time.time() - self.start_time
            }
            
            if self.requests:
                times = [r["response_time"] for r in self.requests]
                stats["avg_response_time"] = sum(times) / len(times)
                stats["min_response_time"] = min(times)
                stats["max_response_time"] = max(times)
            
            return stats

metrics = StressMetrics()

def load_api_key():
    try:
        with open("test_api_key.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        print("✗ test_api_key.txt not found. Run test_setup.py first!")
        exit(1)

prompts = [
    "Hello", "Test", "Hello world", "Query", "Request",
    "What is AI?", "Explain ML", "Cloud computing",
    "Data science", "Big data", "AI safety", "ML models"
]

def stress_worker(api_key, worker_id, duration_seconds, requests_per_second, phase_name):
    """Worker that generates stress by sending rapid requests"""
    print(f"[Stress Worker {worker_id}] Phase: {phase_name}, RPS: {requests_per_second}")
    
    start = time.time()
    request_count = 0
    success_count = 0
    
    while time.time() - start < duration_seconds:
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "prompt": random.choice(prompts),
                "max_tokens": random.randint(20, 100),
                "temperature": random.uniform(0.1, 0.9)
            }
            
            req_start = time.time()
            response = requests.post(
                f"{BASE_URL}/v1/completions",
                json=payload,
                headers=headers,
                timeout=10
            )
            req_time = (time.time() - req_start) * 1000
            
            metrics.record_request(req_time, response.status_code, phase_name)
            
            if response.status_code == 200:
                success_count += 1
            
            request_count += 1
            
            # Pace requests based on RPS target
            if requests_per_second > 0:
                time.sleep(1.0 / requests_per_second / (threading.active_count() / 10 + 1))
        
        except Exception as e:
            metrics.record_request(0, 0, phase_name)
    
    elapsed = time.time() - start
    rps = request_count / elapsed if elapsed > 0 else 0
    print(f"[Stress Worker {worker_id}] Completed: {request_count} requests, {rps:.1f} RPS, {success_count} succeeded")

def phase_ramp_up(api_key, duration_seconds):
    """Phase 1: Gradually increase load"""
    print(f"\n{'='*60}")
    print(f"PHASE 1: RAMP UP (gradual load increase)")
    print(f"Duration: {duration_seconds}s")
    print(f"{'='*60}\n")
    
    start = time.time()
    phase_start_workers = 2
    final_workers = 10
    
    threads = []
    worker_id = 0
    
    steps = int(duration_seconds / 30)  # Increase every 30 seconds
    
    for step in range(steps):
        step_time = time.time() - start
        if step_time >= duration_seconds:
            break
        
        # Calculate how many workers for this step
        progress = step / steps
        num_workers_now = int(phase_start_workers + (final_workers - phase_start_workers) * progress)
        
        print(f"Step {step + 1}: Adding workers (total now: {num_workers_now})")
        
        for i in range(num_workers_now - len(threads)):
            t = threading.Thread(
                target=stress_worker,
                args=(api_key, worker_id, duration_seconds - step_time, 2, "ramp_up")
            )
            t.start()
            threads.append(t)
            worker_id += 1
            time.sleep(1)
        
        time.sleep(30)
    
    # Wait for all threads
    for t in threads:
        t.join()
    
    print(f"Phase 1 Complete\n")

def phase_sustained_high_load(api_key, duration_seconds):
    """Phase 2: Sustained high load"""
    print(f"\n{'='*60}")
    print(f"PHASE 2: SUSTAINED HIGH LOAD")
    print(f"Duration: {duration_seconds}s")
    print(f"Workers: 15")
    print(f"{'='*60}\n")
    
    threads = []
    num_workers = 15
    
    for i in range(num_workers):
        t = threading.Thread(
            target=stress_worker,
            args=(api_key, i, duration_seconds, 3, "sustained_load")
        )
        t.start()
        threads.append(t)
        time.sleep(0.5)
    
    # Print progress
    start = time.time()
    while time.time() - start < duration_seconds:
        elapsed = time.time() - start
        print(f"  Sustained load running... {elapsed:.0f}s / {duration_seconds}s")
        time.sleep(10)
    
    # Wait for all threads
    for t in threads:
        t.join()
    
    print(f"Phase 2 Complete\n")

def phase_burst_traffic(api_key, duration_seconds):
    """Phase 3: Burst traffic (spike pattern)"""
    print(f"\n{'='*60}")
    print(f"PHASE 3: BURST TRAFFIC (spike pattern)")
    print(f"Duration: {duration_seconds}s")
    print(f"{'='*60}\n")
    
    start = time.time()
    burst_num = 0
    burst_interval = 20  # seconds between bursts
    
    while time.time() - start < duration_seconds:
        burst_num += 1
        print(f"BURST #{burst_num} - Starting...")
        
        threads = []
        for i in range(20):  # 20 workers per burst
            t = threading.Thread(
                target=stress_worker,
                args=(api_key, burst_num * 100 + i, 5, 5, "burst")
            )
            t.start()
            threads.append(t)
            time.sleep(0.1)
        
        for t in threads:
            t.join()
        
        print(f"BURST #{burst_num} - Complete")
        
        # Wait before next burst
        remaining = duration_seconds - (time.time() - start)
        if remaining > burst_interval:
            time.sleep(burst_interval)
    
    print(f"Phase 3 Complete\n")

def phase_recovery(api_key, duration_seconds):
    """Phase 4: Recovery (load gradually returns to normal)"""
    print(f"\n{'='*60}")
    print(f"PHASE 4: RECOVERY (gradual load reduction)")
    print(f"Duration: {duration_seconds}s")
    print(f"{'='*60}\n")
    
    start = time.time()
    threads = []
    final_workers = 10
    
    # Start with all workers
    for i in range(final_workers):
        t = threading.Thread(
            target=stress_worker,
            args=(api_key, i, duration_seconds, 2, "recovery")
        )
        t.start()
        threads.append(t)
    
    # Gradually reduce load
    start = time.time()
    while time.time() - start < duration_seconds:
        elapsed = time.time() - start
        print(f"  Recovery in progress... {elapsed:.0f}s / {duration_seconds}s")
        time.sleep(10)
    
    for t in threads:
        t.join()
    
    print(f"Phase 4 Complete\n")

def run_stress_tests():
    """Main stress test orchestration"""
    print(f"\n{'='*60}")
    print(f"STRESS TESTING SCRIPT")
    print(f"{'='*60}")
    print(f"Start Time: {datetime.now().isoformat()}")
    print(f"Total Duration: {TEST_DURATION_MINUTES} minutes")
    print(f"{'='*60}\n")
    
    api_key = load_api_key()
    print(f"✓ Loaded API key\n")
    
    # Allocate time to each phase (approximately)
    phase_duration = int((TEST_DURATION_MINUTES * 60) / 4)
    
    print(f"Phase duration: ~{phase_duration}s each\n")
    
    try:
        # Phase 1: Ramp up
        phase_ramp_up(api_key, phase_duration)
        time.sleep(5)
        
        # Phase 2: Sustained high load
        phase_sustained_high_load(api_key, phase_duration)
        time.sleep(5)
        
        # Phase 3: Burst traffic
        phase_burst_traffic(api_key, phase_duration)
        time.sleep(5)
        
        # Phase 4: Recovery
        phase_recovery(api_key, phase_duration)
    
    except KeyboardInterrupt:
        print("\nStress test interrupted!")
    
    # Print final stats
    print(f"\n{'='*60}")
    print(f"STRESS TEST COMPLETE")
    print(f"{'='*60}")
    stats = metrics.get_stats()
    print(json.dumps(stats, indent=2, default=str))
    print(f"{'='*60}\n")

if __name__ == "__main__":
    run_stress_tests()
