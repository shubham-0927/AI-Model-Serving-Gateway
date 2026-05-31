# Quick Reference Guide

## 🚀 Running Tests

### Option 1: Full Automated (Easiest)
```bash
./run_quick_start.sh
```
Runs complete test suite with prompts and dashboard URLs.

### Option 2: Step by Step
```bash
# 1. Setup (run once)
python3 test_setup.py

# 2. Run individual or all tests
python3 test_load.py          # Load test (20-60 min)
python3 test_resilience.py    # Resilience test (20-60 min)
python3 test_stress.py        # Stress test (20-60 min)

# Or run all in parallel
python3 run_tests.py          # Master orchestration
```

### Option 3: Custom Duration
Edit `test_load.py`, `test_resilience.py`, `test_stress.py`:
```python
TEST_DURATION_MINUTES = 120  # Change to desired duration
```

## 📊 Monitoring During Tests

### Real-Time Metrics
1. **Prometheus**: http://localhost:9090
   - Click "Graph" tab
   - Enter metric names (e.g., `request_latency_ms`)
   - Set time range to "5m" for real-time view

2. **Grafana**: http://localhost:3000
   - Login: admin / admin
   - Create new dashboard
   - Add Prometheus as data source
   - Build panels with queries

3. **Jaeger**: http://localhost:16686
   - Search for traces
   - Filter by service "ai_gateway"
   - View end-to-end request flow

## 📈 Key Metrics to Watch

### Performance
```
avg(request_latency_ms)              # Average response time
histogram_quantile(0.95, request_latency_ms)  # 95th percentile
rate(request_count_total[1m])        # Requests per second
```

### Resilience  
```
increase(fallback_count_total[5m])   # Failovers per 5 minutes
increase(provider_failures_total[5m]) # Provider failures
rate(provider_requests_successful_total[5m]) / rate(provider_requests_total[5m])
```

### Errors
```
rate(request_errors_total[1m])       # Error rate per second
sum(request_errors_total) by (status_code)  # Errors by type
```

## 🔧 Pre-Test Checklist

- [ ] Docker containers running: `docker compose ps`
- [ ] API responding: `curl http://localhost/health`
- [ ] Redis running: `docker compose exec redis redis-cli ping`
- [ ] Postgres running: `docker compose exec postgres psql -U postgres -c "SELECT 1"`
- [ ] Prometheus scraping: http://localhost:9090 shows targets
- [ ] Grafana accessible: http://localhost:3000

## 📝 Log Files

### Container Logs
```bash
docker logs ai_gateway_api -f        # API logs (follow mode)
docker logs ai_gateway_worker -f     # Worker logs
docker logs ai_gateway_beat -f       # Scheduler logs
docker compose logs -f               # All logs
```

### Save Test Output
```bash
python3 test_load.py 2>&1 | tee test_load_$(date +%Y%m%d_%H%M%S).log
```

## 🛠️ Troubleshooting

### API Not Responding
```bash
docker compose restart api
docker logs ai_gateway_api -f
```

### Rate Limiting Too Strict
Check `app/services/rate_limiter.py` for rate limit settings

### Test API Key Not Found
```bash
# Re-run setup
python3 test_setup.py
ls -la test_api_key.txt
```

### Metrics Not Appearing
```bash
# Check Prometheus targets
curl http://localhost:9090/api/v1/targets

# Check metrics endpoint
curl http://localhost/metrics | head -20
```

### Out of Memory
```bash
# Monitor resources
docker stats

# Restart containers if needed
docker compose restart
```

## 🎯 Expected Results

After 60-minute test run, you should see:

✅ **Performance**
- Average latency: 800-1500ms
- P95 latency: 1500-2500ms
- Throughput: 10-20 requests/second

✅ **Reliability**
- Success rate: >95%
- No data loss
- Graceful error handling

✅ **Resilience**
- Automatic failover to alternative providers
- Recovery time: <10 seconds
- No cascading failures

✅ **Scalability**
- Handles 15+ concurrent workers
- Graceful degradation under stress
- Rate limiting prevents overload

## 📚 Documentation Files

- **TEST_SUITE_README.md** - Comprehensive documentation
- **QUICK_REFERENCE.md** - This file
- **test_setup.py** - Environment initialization
- **test_load.py** - Load testing script
- **test_resilience.py** - Resilience testing script
- **test_stress.py** - Stress testing script
- **run_tests.py** - Master orchestration
- **run_quick_start.sh** - Quick start script

## 🚀 Advanced: Custom Scenarios

### High Concurrency Test
Edit `test_load.py`:
```python
NUM_THREADS = 50        # Increase threads
REQUESTS_PER_THREAD = 10  # More requests per thread
```

### Long Duration Test
Edit any test file:
```python
TEST_DURATION_MINUTES = 180  # 3 hours
```

### Specific Provider Testing
Edit `test_load.py`, modify `providers` list:
```python
providers = ["openai"]  # Test only OpenAI
```

### Custom Prompts
Add to prompt list in any test file:
```python
test_prompts = [
    "Your custom prompt here",
    "Another custom prompt"
]
```

## 📞 Debugging Failed Tests

### Enable Debug Logging
```bash
# View raw metrics
curl -s http://localhost/metrics | grep -i error

# Check provider health in Redis
docker compose exec redis redis-cli HGETALL provider:health
```

### Database Queries
```bash
# Connect to database
docker compose exec postgres psql -U postgres -d aigateway

# Check requests table
SELECT COUNT(*) FROM request_logs;
SELECT status_code, COUNT(*) FROM request_logs GROUP BY status_code;
```

### Network Issues
```bash
# Test connectivity from test container
docker compose exec api curl http://localhost:8000/health

# Check DNS
docker compose exec api getent hosts redis postgres
```
