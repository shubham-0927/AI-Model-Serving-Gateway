# 🚀 AI Gateway Test Suite - Complete Setup Guide

## Overview

A comprehensive 60-minute test suite has been created to evaluate your AI Gateway's performance, resilience, and capabilities. The tests generate detailed Prometheus metrics that can be visualized in Grafana.

## 📦 What's Included

### Test Scripts (Executable Python Files)
- **test_setup.py** (3.1 KB) - One-time initialization
  - Creates test user account
  - Generates API key
  - Saves key to `test_api_key.txt`
  
- **test_load.py** (7.9 KB) - Load testing
  - 10 concurrent threads
  - ~5 requests per thread per minute
  - Simulates normal user traffic
  - Measures latency, throughput, success rates
  
- **test_resilience.py** (11 KB) - Resilience testing
  - Provider failover testing
  - Rate limiting verification
  - Concurrent request handling
  - Automatic routing testing
  - Response streaming tests
  
- **test_stress.py** (9.3 KB) - Stress testing
  - Phase 1: Ramp up (gradual load increase)
  - Phase 2: Sustained high load
  - Phase 3: Burst traffic (spike patterns)
  - Phase 4: Recovery (graceful shutdown)

### Orchestration Scripts
- **run_tests.py** (9.3 KB) - Master orchestration
  - Runs all tests in sequence
  - Monitors progress
  - Displays metrics every 60 seconds
  - Takes ~60 minutes total

- **run_quick_start.sh** (2.5 KB) - One-command startup
  - Bash script for easy execution
  - Checks prerequisites
  - Opens monitoring dashboards

### Documentation
- **TEST_SUITE_README.md** (9.6 KB) - Comprehensive guide
  - Detailed instructions
  - Metric interpretation
  - Troubleshooting guide
  
- **QUICK_REFERENCE.md** (5.3 KB) - Quick commands
  - Key commands
  - Expected results
  - Common debugging
  
- **GRAFANA_SETUP.md** (8.2 KB) - Dashboard guide
  - Dashboard templates
  - Query examples
  - Visualization tips

## 🎯 Quick Start (3 Steps)

### Step 1: Verify Docker is Running
```bash
docker compose ps
# You should see containers: api, postgres, redis, prometheus, grafana, worker, beat
```

### Step 2: Execute Tests
```bash
# Option A: Fully automated with prompts
./run_quick_start.sh

# Option B: Direct Python execution
python3 test_setup.py      # Initialize once
python3 run_tests.py       # Run 60-minute test suite
```

### Step 3: Monitor in Real-Time
Open in your browser:
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)
- **Jaeger**: http://localhost:16686

## 📊 Metrics Generated

The test suite automatically generates metrics for:

### Performance Metrics
- Request latency (avg, p50, p95, p99)
- Throughput (requests per second)
- Response time distribution
- Concurrent request handling

### Resilience Metrics
- Failover count (how often providers switched)
- Recovery time (time to restore service)
- Success rates by provider
- Error rates and types
- Circuit breaker states

### Resource Metrics
- CPU usage
- Memory consumption
- Database connections
- Redis operations
- Active streams

### Business Metrics
- Token usage
- Estimated costs
- Rate limit enforcement
- Traffic by tier

## 🔍 What Tests Do

### Load Test (1 hour)
Simulates 10 concurrent users making ~5 requests per minute:
- ✓ Steady state performance
- ✓ Normal latency distribution
- ✓ Throughput capacity
- ✓ Various provider selections
- Result: ~3,000 requests total

### Resilience Test (1 hour)
Tests failure scenarios and recovery:
- ✓ Provider failover behavior
- ✓ Automatic routing intelligence
- ✓ Rate limiting enforcement
- ✓ Concurrent request handling
- ✓ Response streaming
- Result: 200+ resilience checks

### Stress Test (1 hour)
Tests behavior under extreme conditions:
- ✓ Phase 1: Gradual ramp up (2→10 workers)
- ✓ Phase 2: Sustained high load (15 workers)
- ✓ Phase 3: Burst traffic (20 workers, 5-second bursts)
- ✓ Phase 4: Recovery (graceful shutdown)
- Result: Observes system behavior at limits

## 📈 Monitoring During Tests

### Real-Time Console Output
- Progress printed every 60 seconds
- Success/error counts
- Average latency
- Percentile latencies (p95, p99)

### Prometheus Queries (http://localhost:9090)
```
# Response time distribution
histogram_quantile(0.95, request_latency_ms)

# Error rate
sum(rate(request_errors_total[1m])) / sum(rate(request_count_total[1m]))

# Provider health
rate(provider_requests_successful_total[5m]) / rate(provider_requests_total[5m])

# Active connections
active_requests
```

### Grafana Dashboards (http://localhost:3000)
Pre-configured panel templates included in GRAFANA_SETUP.md:
- Performance Overview
- Resilience & Reliability
- Provider Comparison
- System Resources
- Rate Limiting
- Streaming Metrics
- Cost Tracking

## 📋 Files Structure

```
test_setup.py              - Initialize test environment
test_load.py              - Load testing script
test_resilience.py        - Resilience testing script
test_stress.py            - Stress testing script
run_tests.py              - Master orchestration
run_quick_start.sh        - Quick start bash script
test_api_key.txt          - Generated API key (created by setup)

TEST_SUITE_README.md      - Full documentation
QUICK_REFERENCE.md        - Command reference
GRAFANA_SETUP.md          - Dashboard setup guide
```

## 🎓 Understanding Results

### Good Signs (What to Expect)
- ✅ Average latency: 800-1500ms
- ✅ P95 latency: 1500-2500ms
- ✅ Success rate: >95%
- ✅ Throughput: 10-20 RPS
- ✅ Recovery time: <10 seconds
- ✅ No data loss

### Performance Issues (Red Flags)
- ❌ Avg latency >3000ms
- ❌ Success rate <90%
- ❌ Frequent timeouts
- ❌ Memory leaks
- ❌ Database connection errors
- ❌ Unable to handle >5 concurrent users

## 🔧 Customization

### Test Duration
Edit any test file, change:
```python
TEST_DURATION_MINUTES = 60  # Change to desired duration
```

### Concurrency Level
In `test_load.py`:
```python
NUM_THREADS = 10  # Increase for more concurrent users
```

### Request Rate
In `test_load.py`:
```python
REQUESTS_PER_THREAD = 5  # Requests per minute per thread
```

### Custom Prompts
Edit `test_prompts` list in any test file

## 🚨 Troubleshooting

### API Not Responding
```bash
docker compose logs api -f
docker compose restart api
```

### API Key Generation Fails
```bash
python3 test_setup.py
# Re-run to regenerate
```

### Metrics Not Appearing in Prometheus
```bash
# Check if metrics endpoint is responding
curl http://localhost/metrics | head -20

# Check Prometheus targets
curl http://localhost:9090/api/v1/targets
```

### Database Errors
```bash
docker compose exec postgres psql -U postgres -d aigateway -c "SELECT 1"
# Verify connection
```

### Out of Memory
```bash
docker stats
docker compose restart api
```

## 📊 Expected Dashboard Views

### During Load Test
- Steady increasing request rate
- Consistent P95 latency
- 200 status codes dominate
- Occasional 429 rate limit responses

### During Resilience Test
- Spike in failover count when triggered
- Quick recovery to normal latency
- High success rate despite failures
- Mix of provider selection strategies

### During Stress Test
- Phase 1: Linear latency increase
- Phase 2: High latency plateau
- Phase 3: Latency spikes during bursts
- Phase 4: Smooth recovery

## 🎯 Next Steps After Testing

1. **Review Dashboards**
   - Screenshot key metrics
   - Identify performance bottlenecks
   - Note resilience behavior

2. **Analyze Results**
   - Compare against baseline
   - Identify outliers
   - Document findings

3. **Optimize & Re-test**
   - Apply optimizations
   - Run tests again
   - Compare metrics

4. **Production Readiness**
   - Verify all resilience mechanisms work
   - Confirm SLA compliance
   - Document capacity limits

## 📞 Support Resources

- **Prometheus**: http://localhost:9090/graph
- **Grafana**: http://localhost:3000
- **Jaeger**: http://localhost:16686
- **Metrics**: http://localhost/metrics
- **Logs**: `docker logs <container_name>`

## 🎉 You're All Set!

The test suite is ready to run. Choose your preferred start method:

```bash
# Method 1: Guided bash script
./run_quick_start.sh

# Method 2: Direct Python execution
python3 test_setup.py && python3 run_tests.py

# Method 3: Individual tests
python3 test_setup.py
python3 test_load.py &
python3 test_resilience.py &
python3 test_stress.py &
```

Each method takes approximately **60 minutes** to complete.

---

**Created**: 2026-05-31  
**Duration**: ~60 minutes per full run  
**Metrics Resolution**: 5-second intervals  
**Metric Retention**: ~15 days in Prometheus  
**Total Test Coverage**: Load, Resilience, Stress scenarios  
