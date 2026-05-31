# 📑 AI Gateway Test Suite - Complete Index

## 🎯 Start Here
- **START_HERE.md** - Read this first! Quick overview and getting started

## 🚀 Executable Test Scripts
All scripts are executable and ready to run:

1. **test_setup.py** (Run Once)
   - Creates test user and API key
   - Command: `python3 test_setup.py`

2. **test_load.py** (20-60 minutes)
   - Load testing with steady user traffic
   - 10 concurrent threads, ~5 requests/minute/thread
   - Command: `python3 test_load.py`

3. **test_resilience.py** (20-60 minutes)
   - Tests failover, recovery, rate limiting, streaming
   - Multiple test scenarios in cycles
   - Command: `python3 test_resilience.py`

4. **test_stress.py** (20-60 minutes)
   - Ramp-up, sustained load, bursts, recovery phases
   - Tests system behavior under extreme conditions
   - Command: `python3 test_stress.py`

5. **run_tests.py** (Master Orchestrator)
   - Runs all tests sequentially
   - Total ~60 minutes
   - Command: `python3 run_tests.py`

6. **run_quick_start.sh** (One-Command Start)
   - Automated setup and test execution
   - Prerequisites check included
   - Command: `./run_quick_start.sh`

## 📚 Documentation Files

### Essential Reading
- **START_HERE.md** - Quick start guide (read first!)
- **README_TEST_SUITE.md** - Complete setup and usage guide

### Reference Materials
- **QUICK_REFERENCE.md** - Common commands and troubleshooting
- **GRAFANA_SETUP.md** - Dashboard creation and query examples
- **TEST_SUITE_README.md** - Detailed test explanations

## 🚀 Getting Started

### Quick Path (5 minutes)
1. Read START_HERE.md
2. Run: `./run_quick_start.sh`
3. Open monitoring dashboards

### Detailed Path (15 minutes)
1. Read START_HERE.md
2. Read README_TEST_SUITE.md
3. Read GRAFANA_SETUP.md
4. Run: `python3 test_setup.py` then `python3 run_tests.py`
5. Create Grafana dashboards using GRAFANA_SETUP.md

### Custom Path
1. Read QUICK_REFERENCE.md for common commands
2. Customize test_*.py files as needed
3. Run individual tests as desired

## 📊 Monitoring URLs

During tests, open these in your browser:

- **Prometheus**: http://localhost:9090
  - Raw metrics, queries, graphs
  
- **Grafana**: http://localhost:3000
  - Beautiful dashboards
  - Username: admin
  - Password: admin
  
- **Jaeger**: http://localhost:16686
  - Request tracing and analysis

## 📈 Key Metrics

- `request_latency_ms` - Response time
- `request_count_total` - Total requests
- `active_requests` - Current concurrent requests
- `provider_failures_total` - Provider failures
- `fallback_count_total` - Failover events
- `stream_failures_total` - Streaming errors
- `token_usage_total` - Token consumption

## 🎯 What Each Test Does

### Load Test
- Tests normal user traffic
- 10 concurrent threads
- ~5 requests per minute per thread
- Measures latency distribution
- Tests both specific and automatic provider selection

### Resilience Test
- Provider failover scenarios
- Rate limiting enforcement
- Concurrent request handling
- Automatic routing verification
- Response streaming tests
- Runs multiple scenarios in cycles

### Stress Test
- **Phase 1**: Ramp up (2→10 workers over ~15 min)
- **Phase 2**: Sustained high load (15 workers for ~15 min)
- **Phase 3**: Burst traffic (20 workers in 5-sec bursts for ~15 min)
- **Phase 4**: Recovery (gradual shutdown over ~15 min)

## ✅ Expected Results

### Performance
- Average latency: 800-1500ms
- P95 latency: 1500-2500ms
- Throughput: 10-20 RPS
- Success rate: >95%

### Resilience
- Automatic failover works
- Recovery within seconds
- No data loss
- Graceful error handling

### Scalability
- Handles 10+ concurrent users
- No memory leaks
- Proper resource cleanup

## 🔧 Customization

### Change Duration
Edit any test file:
```python
TEST_DURATION_MINUTES = 120  # Change to desired duration
```

### Change Concurrency
In test_load.py:
```python
NUM_THREADS = 50  # Increase for more concurrent users
```

### Custom Prompts
Edit `test_prompts` list in test files

## 📁 File Organization

```
test_setup.py              - Initialize environment
test_load.py              - Load testing
test_resilience.py        - Resilience testing
test_stress.py            - Stress testing
run_tests.py              - Master orchestration
run_quick_start.sh        - Quick start

START_HERE.md             - Read first!
README_TEST_SUITE.md      - Complete guide
GRAFANA_SETUP.md          - Dashboard setup
QUICK_REFERENCE.md        - Quick help
TEST_SUITE_README.md      - Detailed docs
INDEX.md                  - This file
```

## 🛠️ Troubleshooting

### Issues?
1. Check QUICK_REFERENCE.md
2. Check Docker logs: `docker logs ai_gateway_api -f`
3. Verify API: `curl http://localhost/health`
4. Check Redis: `docker compose exec redis redis-cli ping`

## 📞 Common Commands

### Setup
```bash
python3 test_setup.py
```

### Run All Tests
```bash
python3 run_tests.py
```

### Quick Start
```bash
./run_quick_start.sh
```

### Individual Tests
```bash
python3 test_load.py
python3 test_resilience.py
python3 test_stress.py
```

### View Logs
```bash
docker logs ai_gateway_api -f
docker compose logs -f
```

### Check Services
```bash
docker compose ps
curl http://localhost/health
```

## 🎉 Next Steps

1. **Read** START_HERE.md
2. **Run** `./run_quick_start.sh`
3. **Monitor** http://localhost:3000 and http://localhost:9090
4. **Wait** ~60 minutes for tests to complete
5. **Review** metrics and results
6. **Optimize** based on findings

---

**Duration**: ~60 minutes
**Metrics**: 5-second intervals
**Retention**: ~15 days in Prometheus
**Visualization**: Grafana dashboards
