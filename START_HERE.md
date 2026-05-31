# 🎯 START HERE - AI Gateway Test Suite

## Welcome! 👋

You now have a **complete 60-minute test suite** for your AI Gateway. This generates comprehensive metrics to visualize in Grafana/Prometheus, demonstrating your app's performance, resilience, and capabilities.

## ⏱️ What This Does

- **Tests Performance**: Load testing under steady user traffic
- **Tests Resilience**: Failover, recovery, and error handling  
- **Tests Stress**: Behavior under high load and burst traffic
- **Generates Metrics**: Prometheus metrics every 5 seconds
- **Duration**: ~60 minutes total

## 🚀 Quick Start (Choose One)

### Option A: Fully Automated (Recommended)
```bash
./run_quick_start.sh
```
This script:
- Checks prerequisites
- Sets up test user
- Runs all tests
- Shows monitoring dashboard URLs

### Option B: Step by Step
```bash
# Step 1: Initialize test environment (run once)
python3 test_setup.py

# Step 2: Run all tests
python3 run_tests.py

# That's it! Tests run for ~60 minutes
```

### Option C: Individual Tests
```bash
# Setup first
python3 test_setup.py

# Then run any test:
python3 test_load.py          # 20-60 min load test
python3 test_resilience.py    # 20-60 min resilience test  
python3 test_stress.py        # 20-60 min stress test
```

## 📊 Monitor in Real-Time

Open these URLs while tests run:

1. **Prometheus** (Raw Metrics)
   - URL: http://localhost:9090
   - View: Click "Graph" tab, enter metric name
   - Example: `request_latency_ms`

2. **Grafana** (Beautiful Dashboards)
   - URL: http://localhost:3000
   - Username: `admin`
   - Password: `admin`
   - Create dashboards with Prometheus queries

3. **Jaeger** (Request Tracing)
   - URL: http://localhost:16686
   - View: End-to-end request flows

## 📚 Documentation Map

| File | Purpose | Read When |
|------|---------|-----------|
| **README_TEST_SUITE.md** | Complete guide | First - explains everything |
| **QUICK_REFERENCE.md** | Commands & troubleshooting | Need quick answers |
| **GRAFANA_SETUP.md** | Dashboard templates | Want to visualize metrics |
| **TEST_SUITE_README.md** | Detailed explanations | Need deep understanding |
| **QUICK_REFERENCE.md** | Common issues | Something isn't working |

## ✅ Pre-Flight Checklist

Before starting tests:

```bash
# 1. Check Docker is running
docker compose ps
# You should see: api, postgres, redis, prometheus, grafana, worker, beat

# 2. Check API is responding
curl http://localhost/health
# Should return: {"status":"ok"}

# 3. Check Prometheus is scraping
curl -s http://localhost:9090/api/v1/targets | grep "ai_gateway"
# Should show active targets

# 4. Verify redis works
docker compose exec redis redis-cli ping
# Should return: PONG
```

## 🎬 What Happens During Each Test

### Load Test (20 minutes)
- 10 concurrent users
- ~5 requests per user per minute
- Tests: Normal latency, throughput, success rates
- Output: ~1,200 total requests

### Resilience Test (20 minutes)
- Provider failover scenarios
- Rate limiting tests
- Concurrent request handling
- Automatic routing verification
- Streaming response tests

### Stress Test (20 minutes)
- **Phase 1**: Gradually increase load
- **Phase 2**: Sustained high load
- **Phase 3**: Burst traffic spikes
- **Phase 4**: Graceful recovery

## 📈 Key Metrics to Watch

```
request_latency_ms             # Response time in ms
active_requests                # Current concurrent requests
provider_failures_total        # How many provider failures
fallback_count_total           # How many failovers
stream_failures_total          # Streaming errors
```

## 🎯 Expected Results

After 60 minutes, you should see:

✅ **Performance**
- Avg latency: 800-1500ms
- P95 latency: 1500-2500ms  
- Throughput: 10-20 requests/second

✅ **Reliability**
- Success rate: >95%
- Error handling works
- No data loss

✅ **Resilience**
- Automatic failover to backup providers
- Recovery within seconds
- Graceful error handling

✅ **Scalability**
- Handles 10+ concurrent users
- No memory leaks
- Proper resource cleanup

## 🛠️ Troubleshooting

### API not responding?
```bash
docker compose logs api -f
docker compose restart api
```

### API key error?
```bash
python3 test_setup.py
# Re-run to regenerate
```

### Metrics not showing?
```bash
# Check metrics endpoint
curl http://localhost/metrics | head -10

# Check Prometheus is scraping
http://localhost:9090/targets
```

### Tests too slow?
Check Docker resource limits:
```bash
docker stats
# Monitor CPU, memory usage
```

## 📊 Creating Your First Dashboard

1. Open Grafana: http://localhost:3000
2. Login: admin / admin
3. Click "+" (Create)
4. Select "Dashboard"
5. Click "Add Panel"
6. Enter this query: `request_latency_ms`
7. Click outside query box to see data
8. Set title: "Request Latency"
9. Save dashboard

## ⏭️ What's Next?

1. **Run tests**: `./run_quick_start.sh`
2. **Watch dashboards**: Open http://localhost:3000 and http://localhost:9090
3. **Read docs**: Open `GRAFANA_SETUP.md` for dashboard templates
4. **Analyze**: Review metrics after tests complete
5. **Optimize**: Identify bottlenecks and improve

## 📋 File Structure

```
test_setup.py              ← Run this first
test_load.py              ← Load test
test_resilience.py        ← Resilience test
test_stress.py            ← Stress test  
run_tests.py              ← Orchestrator
run_quick_start.sh        ← One-command start

README_TEST_SUITE.md      ← Read this for details
GRAFANA_SETUP.md          ← For visualizations
QUICK_REFERENCE.md        ← For quick help
```

## 🎉 You're Ready!

Choose your method:

```bash
# Automated (easiest)
./run_quick_start.sh

# Manual
python3 test_setup.py
python3 run_tests.py
```

Tests will run for ~60 minutes, generating metrics every 5 seconds.

**Happy testing!** 🚀

---

Questions? Check:
- QUICK_REFERENCE.md - Common commands
- GRAFANA_SETUP.md - Dashboard help
- TEST_SUITE_README.md - Detailed info
