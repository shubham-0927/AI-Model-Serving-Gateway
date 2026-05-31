# Grafana Dashboard Setup Guide

This guide helps you create effective Grafana dashboards to visualize your AI Gateway's performance, resilience, and capabilities during the test run.

## 📊 Initial Setup

### 1. Access Grafana
- URL: `http://localhost:3000`
- Username: `admin`
- Password: `admin`

### 2. Add Prometheus Data Source
1. Click Configuration (gear icon) → Data Sources
2. Click "Add data source"
3. Select "Prometheus"
4. Set URL to: `http://prometheus:9090`
5. Click "Save & Test"

## 🎨 Recommended Dashboards

### Dashboard 1: Performance Overview

**Purpose**: Monitor request latency and throughput

**Panels**:

1. **Average Response Time** (Graph)
   ```
   avg(rate(request_latency_ms[1m]))
   ```
   - Title: "Average Response Time (ms)"
   - Y-axis: milliseconds
   - Refresh: 5s

2. **Request Latency Percentiles** (Graph)
   ```
   histogram_quantile(0.50, rate(request_latency_ms[1m]))
   histogram_quantile(0.95, rate(request_latency_ms[1m]))
   histogram_quantile(0.99, rate(request_latency_ms[1m]))
   ```
   - Title: "Response Time Percentiles"
   - Legend: P50, P95, P99
   - Refresh: 5s

3. **Throughput** (Graph)
   ```
   sum(rate(request_count_total[1m]))
   ```
   - Title: "Requests Per Second"
   - Y-axis: RPS
   - Refresh: 5s

4. **Active Requests** (Gauge)
   ```
   active_requests
   ```
   - Title: "Active Concurrent Requests"
   - Thresholds: Green (0-100), Yellow (100-500), Red (500+)
   - Refresh: 5s

### Dashboard 2: Resilience & Reliability

**Purpose**: Monitor failover, recovery, and error handling

**Panels**:

1. **Success Rate** (Stat)
   ```
   sum(rate(request_count_total{status_code="200"}[5m])) / sum(rate(request_count_total[5m])) * 100
   ```
   - Title: "Success Rate (%)"
   - Color Mode: Gradient
   - Thresholds: 95 (green), 90 (yellow), 85 (red)

2. **Failover Events** (Counter)
   ```
   increase(fallback_count_total[5m])
   ```
   - Title: "Failovers (Last 5 min)"
   - Refresh: 5s

3. **Provider Failures** (Counter)
   ```
   increase(provider_failures_total[5m])
   ```
   - Title: "Provider Failures (Last 5 min)"
   - By Provider (use `by (provider)` clause)

4. **Error Distribution** (Pie Chart)
   ```
   sum(request_errors_total) by (status_code)
   ```
   - Title: "Errors by Status Code"
   - Show Legend: Yes

5. **Circuit Breaker Status** (Graph)
   ```
   circuit_breaker_state
   ```
   - Title: "Provider Circuit Breaker States"
   - By Provider
   - Values: CLOSED (1), HALF_OPEN (2), OPEN (3)

### Dashboard 3: Provider Performance

**Purpose**: Compare performance across different AI providers

**Panels**:

1. **Provider Response Times** (Graph)
   ```
   avg(rate(provider_latency_ms[1m])) by (provider)
   ```
   - Title: "Response Time by Provider"
   - Legend: Show provider names

2. **Provider Success Rates** (Bar Chart)
   ```
   sum(rate(provider_requests_successful_total[5m])) by (provider) / 
   sum(rate(provider_requests_total[5m])) by (provider) * 100
   ```
   - Title: "Provider Success Rate (%)"
   - Values: Success rate per provider

3. **Provider Request Volume** (Bar Chart)
   ```
   sum(rate(provider_requests_total[1m])) by (provider)
   ```
   - Title: "Request Volume by Provider"

4. **Provider Health Score** (Gauge)
   ```
   provider_health_score
   ```
   - Title: "Provider Health Scores"
   - By Provider
   - Thresholds: 0.8 (green), 0.6 (yellow), 0.4 (red)

### Dashboard 4: System Resources

**Purpose**: Monitor resource utilization

**Panels**:

1. **API Request Rate** (Graph)
   ```
   rate(request_count_total[1m])
   ```

2. **Database Connections** (Gauge)
   ```
   db_connection_pool_size
   ```
   - Title: "Active DB Connections"

3. **Redis Commands/sec** (Graph)
   ```
   rate(redis_commands_total[1m])
   ```

4. **Memory Usage Trend** (Graph)
   ```
   process_resident_memory_bytes / 1024 / 1024
   ```
   - Title: "Memory Usage (MB)"

5. **CPU Usage** (Graph)
   ```
   process_cpu_seconds_total
   ```
   - Title: "CPU Seconds"

### Dashboard 5: Rate Limiting & Admission Control

**Purpose**: Monitor rate limiting effectiveness

**Panels**:

1. **Rate Limited Requests** (Counter)
   ```
   increase(request_errors_total{status_code="429"}[5m])
   ```
   - Title: "Rate Limited Requests (Last 5 min)"

2. **Rate Limit Rejections by Tier** (Bar Chart)
   ```
   sum(request_errors_total{status_code="429"}) by (tier)
   ```
   - Title: "Rate Limit Rejections by Tier"

3. **Admission Control Rejections** (Counter)
   ```
   increase(admission_control_rejections_total[5m])
   ```
   - Title: "Admission Control Rejections"

4. **Requests by Tier** (Pie Chart)
   ```
   sum(rate(request_count_total[5m])) by (tier)
   ```
   - Title: "Traffic Distribution by Tier"

### Dashboard 6: Streaming & Long-Running Requests

**Purpose**: Monitor streaming behavior

**Panels**:

1. **Active Streams** (Gauge)
   ```
   active_streams
   ```
   - Title: "Active Streaming Connections"

2. **Stream Duration** (Graph)
   ```
   histogram_quantile(0.95, rate(stream_duration_seconds[1m]))
   ```
   - Title: "Stream Duration P95 (seconds)"

3. **Stream Failures** (Counter)
   ```
   increase(stream_failures_total[5m])
   ```
   - Title: "Stream Failures (Last 5 min)"

4. **Tokens Streamed** (Counter)
   ```
   increase(tokens_streamed_total[5m])
   ```
   - Title: "Tokens Streamed (Last 5 min)"

### Dashboard 7: Cost & Usage Tracking

**Purpose**: Monitor token usage and estimated costs

**Panels**:

1. **Total Tokens Used** (Counter)
   ```
   sum(token_usage_total)
   ```
   - Title: "Total Tokens Used"

2. **Tokens by Provider** (Bar Chart)
   ```
   sum(token_usage_total) by (provider)
   ```
   - Title: "Token Usage by Provider"

3. **Estimated Cost** (Stat)
   ```
   sum(estimated_cost_total)
   ```
   - Title: "Estimated Cost"
   - Unit: $

4. **Cost Trend** (Graph)
   ```
   sum(rate(estimated_cost_total[1h])) * 3600
   ```
   - Title: "Estimated Hourly Cost"

## 🔄 Multi-Tenant Dashboard

If testing with multiple users:

```
sum(rate(request_count_total[1m])) by (user_id)
sum(rate(request_errors_total[1m])) by (user_id)
avg(request_latency_ms) by (user_id)
```

## 📊 Creating a Custom Query

1. Go to any dashboard
2. Click "New Panel" → "Add Panel"
3. In query editor, click on "Prometheus"
4. Enter a metric name or use autocompletion
5. Use functions like:
   - `rate()` - requests per second
   - `increase()` - total growth
   - `avg()` - average value
   - `sum()` - total value
   - `histogram_quantile()` - percentiles

## 📈 Query Tips

### Time Range Aggregation
```
[5m]   # Last 5 minutes
[1h]   # Last hour
[1d]   # Last day
```

### Grouping
```
by (label_name)              # Group by single label
by (label1, label2)          # Group by multiple labels
without (label_name)         # Exclude label from grouping
```

### Math Operations
```
a / b * 100                  # Calculate percentage
(a - b) / b * 100            # Percentage change
```

### Examples
```
# Error rate
sum(rate(errors[5m])) / sum(rate(requests[5m])) * 100

# Latency by provider
histogram_quantile(0.95, rate(latency[5m])) by (provider)

# Uptime percentage
up * 100
```

## 🎯 Dashboard Organization

Create folders for different aspects:

1. **Performance** - Latency, throughput, resources
2. **Reliability** - Errors, failures, recovery
3. **Providers** - Per-provider metrics
4. **Business** - Costs, usage, quotas
5. **Debugging** - Detailed technical metrics

## 💾 Saving Dashboards

Dashboards are auto-saved in Grafana database. To export:
1. Open dashboard
2. Click dashboard title
3. Select "Share" → "Export" → "Copy JSON"

To import:
1. Click + (Create) → Import
2. Paste JSON
3. Select Prometheus data source
4. Click Import

## 🔔 Alerting

To set up alerts:
1. Open any panel
2. Click panel title → Edit
3. Go to Alert tab
4. Set threshold (e.g., error rate > 5%)
5. Add notification channel

## 📞 Useful Metric Names

```
request_*                    # Request metrics
provider_*                   # Provider-specific metrics
stream_*                     # Streaming metrics
token_*                      # Token usage
rate_limit_*                 # Rate limiting
circuit_breaker_*            # Circuit breaker state
admission_control_*          # Admission control
```

View all available metrics at: `http://localhost:9090/api/v1/label/__name__/values`
