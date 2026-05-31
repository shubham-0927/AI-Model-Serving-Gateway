#!/usr/bin/env python3
"""
Master Test Orchestration Script
Runs the complete test suite and monitors results
"""

import subprocess
import os
import sys
import time
from datetime import datetime, timedelta
import json

def print_header(title):
    """Print formatted header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def print_section(title):
    """Print formatted section"""
    print(f"\n{'-'*70}")
    print(f"  {title}")
    print(f"{'-'*70}\n")

def run_command(cmd, description):
    """Run a shell command"""
    print(f"[{datetime.now().isoformat()}] {description}")
    print(f"Command: {cmd}\n")
    
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0

def check_docker_containers():
    """Check if docker containers are running"""
    print_section("CHECKING DOCKER CONTAINERS")
    
    containers = [
        "ai_gateway_api",
        "ai_gateway_postgres", 
        "ai_gateway_redis",
        "ai_gateway_prometheus",
        "ai_gateway_grafana",
        "ai_gateway_worker",
        "ai_gateway_beat"
    ]
    
    for container in containers:
        cmd = f"docker ps --filter 'name={container}' --format '{{{{.Names}}}}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        status = "✓ RUNNING" if container in result.stdout else "✗ STOPPED"
        print(f"  {container}: {status}")

def wait_for_api():
    """Wait for API to be ready"""
    print_section("WAITING FOR API TO BE READY")
    
    import requests
    max_retries = 30
    
    for attempt in range(max_retries):
        try:
            response = requests.get("http://localhost/health", timeout=5)
            if response.status_code == 200:
                print(f"✓ API is ready!\n")
                return True
        except Exception as e:
            pass
        
        if attempt < max_retries - 1:
            print(f"  Attempt {attempt + 1}/{max_retries}: Waiting for API...")
            time.sleep(2)
    
    print(f"✗ API is not responding after {max_retries} attempts")
    return False

def run_test_setup():
    """Run test setup to create user and API key"""
    print_section("RUNNING TEST SETUP")
    return run_command(
        "python3 test_setup.py",
        "Creating test user and API key..."
    )

def run_load_test(duration_minutes=20):
    """Run load test"""
    print_section(f"RUNNING LOAD TEST ({duration_minutes} minutes)")
    
    # Modify test_load.py temporarily to use the specified duration
    cmd = f"python3 test_load.py"
    return run_command(cmd, "Executing load test...")

def run_resilience_test(duration_minutes=20):
    """Run resilience test"""
    print_section(f"RUNNING RESILIENCE TEST ({duration_minutes} minutes)")
    return run_command(
        "python3 test_resilience.py",
        "Executing resilience test..."
    )

def run_stress_test(duration_minutes=20):
    """Run stress test"""
    print_section(f"RUNNING STRESS TEST ({duration_minutes} minutes)")
    return run_command(
        "python3 test_stress.py",
        "Executing stress test..."
    )

def monitor_metrics():
    """Print access instructions for monitoring"""
    print_section("MONITORING DASHBOARDS")
    
    print("""
Access the following dashboards to view real-time metrics:

1. PROMETHEUS (Metrics Database)
   URL: http://localhost:9090
   Purpose: View raw metrics and perform queries
   Useful Queries:
     - request_latency_ms
     - request_count_total
     - active_requests
     - provider_failures_total
     - fallback_count_total

2. GRAFANA (Visualization)
   URL: http://localhost:3000
   Default Login: admin / admin
   Purpose: View dashboards and visualizations
   
   Expected Dashboards:
     - Request Performance (latency, throughput)
     - Provider Health (success rates, availability)
     - System Resources (CPU, memory, connections)
     - Error Rates (failures, timeouts)
     - Resilience Metrics (failovers, recovery time)

3. JAEGER (Distributed Tracing)
   URL: http://localhost:16686
   Purpose: Trace individual requests end-to-end
   Useful for: Understanding request flow and latency distribution

4. METRICS ENDPOINT (Direct)
   URL: http://localhost/metrics
   Purpose: Prometheus format metrics export
""")

def print_final_summary(start_time):
    """Print final test summary"""
    print_header("TEST EXECUTION COMPLETE")
    
    elapsed = time.time() - start_time
    hours = int(elapsed // 3600)
    minutes = int((elapsed % 3600) // 60)
    seconds = int(elapsed % 60)
    
    print(f"""
Total Execution Time: {hours:02d}:{minutes:02d}:{seconds:02d}

Next Steps:
1. Review metrics in Prometheus and Grafana
2. Analyze response times and error rates
3. Check provider failover behavior
4. Verify rate limiting effectiveness
5. Assess system resilience under stress

Data Retention:
- Prometheus data: ~15 days (default retention)
- Application logs: Check container logs with 'docker logs <container>'
- Test results: Saved in current directory

To view container logs:
  docker logs ai_gateway_api -f
  docker logs ai_gateway_worker -f
  docker logs ai_gateway_beat -f

To access database directly:
  docker compose exec postgres psql -U postgres -d aigateway

To reset and restart:
  docker compose down -v
  docker compose up --build
""")

def main():
    """Main orchestration logic"""
    print_header("AI GATEWAY - COMPREHENSIVE TEST SUITE (60 MINUTES)")
    
    start_time = time.time()
    end_time = start_time + (60 * 60)  # 60 minutes
    
    print(f"Start Time: {datetime.now().isoformat()}")
    print(f"End Time: {datetime.fromtimestamp(end_time).isoformat()}")
    print(f"\nThis test suite will:")
    print(f"  ✓ Verify API is running")
    print(f"  ✓ Set up test user and API key")
    print(f"  ✓ Run load tests (normal traffic)")
    print(f"  ✓ Run resilience tests (failover, recovery)")
    print(f"  ✓ Run stress tests (high load)")
    print(f"  ✓ Generate Prometheus/Grafana metrics")
    print(f"\nAll tests will run concurrently to fill the hour with diverse workloads.")
    
    # Check Docker containers
    check_docker_containers()
    
    # Wait for API
    if not wait_for_api():
        print("✗ Cannot proceed without API")
        sys.exit(1)
    
    # Run setup
    if not run_test_setup():
        print("✗ Test setup failed")
        sys.exit(1)
    
    print_section("STARTING CONCURRENT TEST EXECUTION")
    print(f"Duration: 60 minutes\n")
    
    # Start all tests as background processes
    processes = []
    
    print(f"Starting tests at {datetime.now().isoformat()}...\n")
    
    # We'll run tests sequentially for clarity, but they could be run in parallel
    # Allocate roughly 20 minutes each for load, resilience, and stress tests
    
    print("Starting Load Test (20 minutes)...")
    # Modify duration in test_load.py to 20 minutes
    load_process = subprocess.Popen(["python3", "test_load.py"])
    processes.append(("Load Test", load_process))
    
    # Let it run, then start next one
    time.sleep(120)  # Let it stabilize
    
    print("Starting Resilience Test (20 minutes)...")
    resilience_process = subprocess.Popen(["python3", "test_resilience.py"])
    processes.append(("Resilience Test", resilience_process))
    
    time.sleep(120)  # Let it stabilize
    
    print("Starting Stress Test (20 minutes)...")
    stress_process = subprocess.Popen(["python3", "test_stress.py"])
    processes.append(("Stress Test", stress_process))
    
    # Monitor while tests are running
    print_section("TESTS RUNNING")
    print(f"""
The following tests are now running:
  1. Load Test (simulating steady user traffic)
  2. Resilience Test (testing failover and recovery)
  3. Stress Test (burst traffic and high load)

Open monitoring dashboards in your browser:
  - Prometheus: http://localhost:9090
  - Grafana: http://localhost:3000
  - Jaeger: http://localhost:16686
""")
    
    # Wait for all processes to complete
    remaining = end_time - time.time()
    print(f"Estimated remaining time: {int(remaining / 60)} minutes\n")
    
    all_completed = False
    while time.time() < end_time and not all_completed:
        all_completed = True
        for name, process in processes:
            if process.poll() is None:
                all_completed = False
                elapsed = time.time() - start_time
                remaining = end_time - time.time()
                print(f"[{datetime.now().isoformat()}] "
                      f"Tests running... "
                      f"Elapsed: {int(elapsed/60)}m, "
                      f"Remaining: {int(remaining/60)}m")
            else:
                print(f"[{datetime.now().isoformat()}] {name} completed")
        
        if not all_completed:
            time.sleep(60)
    
    # Wait for any remaining processes
    for name, process in processes:
        if process.poll() is None:
            print(f"Terminating {name}...")
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
    
    # Show monitoring options
    monitor_metrics()
    
    # Print summary
    print_final_summary(start_time)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest execution interrupted by user")
        sys.exit(0)
