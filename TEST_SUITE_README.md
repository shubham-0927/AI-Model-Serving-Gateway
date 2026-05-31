# AI Gateway - Comprehensive Test Suite

This directory contains a complete test suite to evaluate the AI Model Serving Gateway's performance, resilience, and capabilities over a 60-minute period. The tests generate detailed metrics for visualization in Prometheus and Grafana.

## 📋 Overview

The test suite consists of three main test scenarios:

1. **Load Test** (`test_load.py`) - Simulates steady user traffic
2. **Resilience Test** (`test_resilience.py`) - Tests failover, recovery, and edge cases
3. **Stress Test** (`test_stress.py`) - Tests behavior under high load conditions

All tests generate metrics that can be visualized in Prometheus and Grafana.

## 🚀 Quick Start

### Prerequisites

Ensure the application is running in Docker:

```bash
# Build and start the application
cd /path/to/project
docker compose build
docker compose up --build

# Initialize the database in another terminal
docker compose exec api python -c "from app.db.init_db import init_db; init_db()"
```

### Running the Complete Test Suite (60 minutes)

The easiest way to run all tests:

```bash
# Make scripts executable
chmod +x test_setup.py test_load.py test_resilience.py test_stress.py run_tests.py

# Run the master orchestration script
python3 run_tests.py
```

This will:
1. Verify API is ready
2. Create a test user and API key
3. Start load, resilience, and stress tests
4. Run all tests for approximately 60 minutes
5. Display monitoring dashboard URLs

### Running Individual Tests

#### Step 1: Setup (Required once)

```bash
python3 test_setup.py
```

This creates:
- Test user account
- API key for testing
- Saves API key to `test_api_key.txt`

#### Step 2a: Load Test Only

```bash
# Adjust TEST_DURATION_MINUTES in test_load.py if needed (default: 60)
python3 test_load.py
```

**What it does:**
- Simulates 10 concurrent users
- ~5 requests per user per minute
- Tests both specific provider selection and automatic routing
- Measures latency, throughput, and success rates
- Prints metrics every 60 seconds

#### Step 2b: Resilience Test Only

```bash
python3 test_resilience.py
```

**What it does:**
- Tests provider failover behavior
- Tests rate limiting effectiveness
- Tests concurrent request handling
- Tests automatic routing
- Tests response streaming
- Runs these tests in cycles for 60 minutes

#### Step 2c: Stress Test Only

```bash
python3 test_stress.py
```

**What it does:**
- **Phase 1: Ramp Up** - Gradually increase load from 2 to 10 workers
- **Phase 2: Sustained High Load** - Run 15 workers continuously
- **Phase 3: Burst Traffic** - Simulate traffic spikes with 20 workers
- **Phase 4: Recovery** - Gradually reduce load back to normal

## 📊 Monitoring

### Prometheus
Access at: **http://localhost:9090**

Key metrics to query:
```
# Request latency (percentiles)
histogram_quantile(0.95, request_latency_ms)
histogram_quantile(0.99, request_latency_ms)

# Request rate
rate(request_count_total[1m])

# Active requests
active_requests

# Provider failures
increase(provider_failures_total[5m])

# Fallback usage
increase(fallback_count_total[5m])

# Token usage
token_usage_total

# Stream metrics
stream_count_total
stream_duration_seconds
```

### Grafana
Access at: **http://localhost:3000**

Default credentials: `admin` / `admin`

Expected visualizations:
- Request latency over time (avg, p95, p99)
- Throughput (requests per second)
- Error rates by status code
- Provider health and success rates
- Active connections and resource usage
- Resilience metrics (failovers, recovery time)

To create custom dashboards:
1. Add Prometheus as a data source (http://prometheus:9090)
2. Create panels with the queries listed above
3. Set refresh interval to 5-10 seconds

### Jaeger Tracing
Access at: **http://localhost:16686**

View end-to-end request traces to understand:
- Request flow through the gateway
- Latency breakdown by component
- Provider selection and routing decisions
- Fallback behavior

### Direct Metrics Endpoint
Access at: **http://localhost/metrics**

Raw Prometheus format metrics in text format.

## 📈 What to Expect

### Load Test Results (20 minutes)
- **Total Requests**: ~1,200 (10 threads × 5/min × 20 min)
- **Success Rate**: >95%
- **Average Latency**: 800-1200ms
- **P95 Latency**: 1500-2000ms
- **Status Codes**: 200 (success), occasional 429 (rate limit)

### Resilience Test Results (20 minutes)
- **Failover Success Rate**: >90%
- **Automatic Routing**: Successful provider selection
- **Recovery Time**: <5 seconds on average
- **Concurrent Requests**: Handle 5+ concurrent workers
- **Streaming**: Successful chunk delivery

### Stress Test Results (20 minutes)
- **Phase 1 (Ramp Up)**: Smooth increase in latency as load increases
- **Phase 2 (Sustained High Load)**: Consistent response times, some 429s expected
- **Phase 3 (Burst)**: Spike in latency, recovery within 5-10 seconds
- **Phase 4 (Recovery)**: Smooth decrease in latency

## 🔍 Key Metrics to Monitor

### Performance Metrics
- **Response Time**: Should increase gradually under load
- **Throughput**: Maximum sustainable requests per second
- **P95/P99 Latency**: Tail latency behavior

### Resilience Metrics
- **Failover Count**: How many times gateway switched providers
- **Recovery Time**: Time to recover from failures
- **Success Rate**: Percentage of successful requests

### Resource Metrics
- **Active Requests**: Current concurrent requests
- **Memory Usage**: Process memory over time
- **CPU Usage**: Process CPU consumption
- **Database Connections**: Connection pool usage

### Error Metrics
- **Rate Limit Errors (429)**: Expected under heavy load
- **Server Errors (500)**: Should be minimal
- **Timeout Errors**: Indicate performance issues
- **Provider Failures**: Indicates which providers are unreliable

## 🛠️ Customization

### Adjust Load Parameters

Edit `test_load.py`:
```python
NUM_THREADS = 10              # Number of concurrent threads
REQUESTS_PER_THREAD = 5       # Requests per thread per minute
TEST_DURATION_MINUTES = 60    # Total test duration
```

### Adjust Stress Parameters

Edit `test_stress.py`:
```python
phase_duration = int((TEST_DURATION_MINUTES * 60) / 4)  # ~15 min per phase
num_workers = 15  # Workers in sustained load phase
```

### Custom Test Prompts

Edit the `test_prompts` list in `test_load.py` or test scripts.

## 📋 Test Logs and Results

### Viewing Results

During test execution:
- Console output shows real-time progress
- Metrics are printed every 60 seconds
- Final statistics shown after each test completes

### Saving Results

Results are printed to console. To save:
```bash
python3 run_tests.py 2>&1 | tee test_results_$(date +%s).log
```

### Docker Container Logs

```bash
# API logs
docker logs ai_gateway_api -f

# Worker logs
docker logs ai_gateway_worker -f

# Beat scheduler logs
docker logs ai_gateway_beat -f

# Postgres logs
docker logs ai_gateway_postgres -f

# Redis logs
docker logs ai_gateway_redis -f
```

## ⚙️ Troubleshooting

### API Connection Issues
```bash
# Check if containers are running
docker compose ps

# Check API health
curl http://localhost/health

# Check nginx logs
docker logs ai_gateway_nginx -f
```

### Authentication Failures
```bash
# Verify test_api_key.txt exists
ls -la test_api_key.txt

# Re-run setup
python3 test_setup.py
```

### Low Throughput
- Check if API is under heavy load from other processes
- Monitor CPU and memory usage: `docker stats`
- Check provider simulated latency in `app/simulation/provider_simulation.py`

### Rate Limiting Too Aggressive
- Adjust rate limits in app configuration
- Check Redis is running: `docker compose exec redis redis-cli ping`

### Database Issues
```bash
# Check database status
docker compose exec postgres psql -U postgres -d aigateway -c "SELECT 1"

# View tables
docker compose exec postgres psql -U postgres -d aigateway -c "\dt"
```

## 📚 Key Files

- **test_setup.py** - Initializes test environment (run once)
- **test_load.py** - Simulates normal user load
- **test_resilience.py** - Tests failover and edge cases
- **test_stress.py** - Tests high load conditions
- **run_tests.py** - Master orchestration script
- **test_api_key.txt** - Generated API key (created by test_setup.py)

## 🎯 Success Criteria

Tests should demonstrate:
- ✅ API can handle 10+ concurrent users
- ✅ Response latency remains reasonable (<2000ms p95)
- ✅ Automatic provider routing works
- ✅ Failover to alternative providers when one fails
- ✅ Rate limiting enforced correctly
- ✅ Recovery from failures within seconds
- ✅ Graceful handling of burst traffic
- ✅ Streaming responses work correctly
- ✅ No data corruption or loss

## 📖 Example Grafana Queries

### Average Response Time (Last Hour)
```
avg(rate(request_latency_ms[1m]))
```

### Request Rate
```
sum(rate(request_count_total[1m]))
```

### Error Rate
```
sum(rate(request_errors_total[1m])) / sum(rate(request_count_total[1m]))
```

### Provider Success Rate
```
sum(rate(provider_requests_successful_total[5m])) / sum(rate(provider_requests_total[5m])) by (provider)
```

### Active Connections
```
active_requests
```

## 🚀 Next Steps

After running tests:
1. Review Grafana dashboards for trends
2. Identify performance bottlenecks
3. Optimize based on observed metrics
4. Run tests again after optimizations
5. Compare metrics with baseline

## 📞 Support

For issues or questions:
1. Check container logs: `docker logs <container_name>`
2. Verify connectivity: `curl http://localhost/health`
3. Check Redis: `docker compose exec redis redis-cli ping`
4. Review application logs in app directory

---

**Test Duration**: ~60 minutes
**Generated**: Prometheus metrics every 5 seconds
**Retention**: Prometheus keeps ~15 days of data by default
