# AI Gateway Control Plane

A production-oriented AI Gateway and Orchestration Platform built with FastAPI, Redis, Celery, PostgreSQL, Prometheus, Grafana, and OpenTelemetry.

The system acts as a centralized control plane for AI model providers, handling:

- intelligent request routing
- retries & failover
- rate limiting
- distributed scheduling
- circuit breakers
- observability
- token accounting
- tenant isolation
- queue-based orchestration

The project focuses on distributed systems and AI infrastructure engineering concepts rather than only model inference.

---

# Features

## Gateway & Routing

- FastAPI-based AI Gateway
- Provider Abstraction Layer
- Adaptive Routing Engine
- Load-aware Routing
- Cost-aware Routing
- Reliability-aware Routing
- Streaming Response Support

---

## Reliability Engineering

- Retry Engine with Exponential Backoff
- Circuit Breakers
- Provider Cooldowns
- Failure Recovery
- Chaos Simulation
- Simulated Provider Failures & Latency

---

## Distributed Infrastructure

- Redis-backed Shared State
- Celery Workers & Scheduled Tasks
- Queue-based Request Scheduling
- Priority Queues
- Weighted Fair Scheduling
- Multi-tenant Isolation
- Admission Control & Backpressure

---

## Observability

- Prometheus Metrics
- Grafana Dashboards
- OpenTelemetry Tracing
- Jaeger Distributed Tracing
- Structured Logging
- Queue & Latency Metrics

---

## AI Platform Features

- Token Usage Accounting
- Token Budget Enforcement
- Cost Estimation
- Tier-based Limits
- API Key Authentication
- Tenant-aware Quotas

---

# Architecture

```text
                        +------------------+
                        |      Client      |
                        +---------+--------+
                                  |
                                  v
                   +-----------------------------+
                   |     AI Gateway Control      |
                   |         FastAPI API         |
                   +--------------+--------------+
                                  |
             +--------------------+--------------------+
             |                    |                    |
             v                    v                    v

      +-------------+      +-------------+      +-------------+
      |   OpenAI    |      | Anthropic   |      | Future LLMs |
      |  Provider   |      |  Provider   |      |   Provider  |
      +-------------+      +-------------+      +-------------+

                                  |
                   +-----------------------------+
                   |      Distributed State      |
                   |           Redis             |
                   +-----------------------------+

                                  |
              +--------------------------------------+
              | Background Workers & Scheduling      |
              | Celery + Queue Processing            |
              +--------------------------------------+

                                  |
          +----------------------------------------------+
          | Observability Stack                          |
          | Prometheus + Grafana + Jaeger               |
          +----------------------------------------------+
```

---

# Tech Stack

| Layer | Technologies |
|------|------|
| API Gateway | FastAPI, Uvicorn |
| Distributed State | Redis |
| Background Jobs | Celery |
| Database | PostgreSQL |
| Reverse Proxy | Nginx |
| Observability | Prometheus, Grafana, Jaeger |
| Tracing | OpenTelemetry |
| Containerization | Docker, Docker Compose |

---

# Key Engineering Concepts

This project implements several distributed systems and infrastructure engineering concepts:

- Adaptive Request Routing
- Distributed Circuit Breakers
- Retry & Backoff Strategies
- Queue Scheduling
- Load Shedding
- Admission Control
- Fair Scheduling
- Multi-tenant Isolation
- Token Governance
- Chaos Engineering Simulation
- Observability-driven Infrastructure

---

# Project Structure

```text
app/
├── api/
├── auth/
├── core/
├── providers/
├── routing/
├── registry/
├── simulation/
├── workers/
├── metrics/
├── tracing/
└── scheduling/
```

---

# Running the Project

## Start Services

```bash
docker compose up --build
```

---

## API Docs

```text
http://localhost:8000/docs
```

---

## Grafana Dashboard

```text
http://localhost:3000
```

---

## Prometheus

```text
http://localhost:9090
```

---

## Jaeger Tracing

```text
http://localhost:16686
```

---

# Example Request

```http
POST /v1/completions
```

```json
{
  "prompt": "Explain distributed systems",
  "strategy": "adaptive_routing",
  "stream": false
}
```

---

# Current Capabilities

- Adaptive orchestration
- Distributed scheduling
- Provider health tracking
- Queue-aware traffic smoothing
- Retry & fallback handling
- Tenant-aware quotas
- Streaming support
- Token accounting
- Distributed observability

---

# Future Improvements

- Kubernetes Deployment
- Real LLM Provider Integration
- Semantic Caching
- GPU-aware Scheduling
- ML-driven Routing Policies
- CI/CD Pipelines
- Advanced Benchmarking

---

# Author

Shubham Dewangan