# AI Gateway Control Plane

![AI Gateway Control Plane](https://img.shields.io/badge/AI%20Gateway-%F0%9F%A4%96-blue?style=for-the-badge&logo=ai)

[![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-v0.111-green?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-blue?style=flat-square&logo=docker)](https://www.docker.com/)
[![Redis](https://img.shields.io/badge/Redis-red?style=flat-square&logo=redis)](https://redis.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-blue?style=flat-square&logo=postgresql)](https://www.postgresql.org/)
[![Celery](https://img.shields.io/badge/Celery-5.6.3-brightgreen?style=flat-square&logo=celery)](https://docs.celeryq.dev/)


A production-oriented AI Gateway and orchestration platform for intelligent provider routing, distributed scheduling, and observability.

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

> Focused on infrastructure engineering and reliability for AI systems, rather than only model inference.

---

## 🚀 Highlights

- Adaptive request routing across AI providers
- Failover-aware retry engine with exponential backoff
- Redis-backed shared state and Celery scheduling
- Prometheus + Grafana + Jaeger observability
- Tenant-aware quotas, token accounting, and API key auth

---

## 🧩 Built With

| Category | Technology |
|---|---|
| API | FastAPI, Uvicorn |
| Language | Python 3.12 |
| State | Redis |
| Queueing | Celery |
| Database | PostgreSQL |
| Observability | Prometheus, Grafana, Jaeger |
| Tracing | OpenTelemetry |
| Deployment | Docker, Docker Compose |

---

## 🌐 Features

### Gateway & Routing

- FastAPI-based AI Gateway
- Provider Abstraction Layer
- Adaptive Routing Engine
- Load-aware Routing
- Cost-aware Routing
- Reliability-aware Routing
- Streaming Response Support

### Reliability Engineering

- Retry Engine with Exponential Backoff
- Circuit Breakers
- Provider Cooldowns
- Failure Recovery
- Chaos Simulation
- Simulated Provider Failures & Latency

### Distributed Infrastructure

- Redis-backed Shared State
- Celery Workers & Scheduled Tasks
- Queue-based Request Scheduling
- Priority Queues
- Weighted Fair Scheduling
- Multi-tenant Isolation
- Admission Control & Backpressure

### Observability

- Prometheus Metrics
- Grafana Dashboards
- OpenTelemetry Tracing
- Jaeger Distributed Tracing
- Structured Logging
- Queue & Latency Metrics

### AI Platform Features

- Token Usage Accounting
- Token Budget Enforcement
- Cost Estimation
- Tier-based Limits
- API Key Authentication
- Tenant-aware Quotas

---

## 🏗 Architecture

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

## 📁 Project Structure

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

## ▶️ Running the Project

### Start Services

```bash
docker compose up --build
```

### API Docs

http://localhost:8000/docs

### Grafana Dashboard

http://localhost:3000

### Prometheus

http://localhost:9090

### Jaeger Tracing

http://localhost:16686

---

## 🧪 Example Request

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

## 💡 Current Capabilities

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

## 🔮 Future Improvements

- Kubernetes Deployment
- Real LLM Provider Integration
- Semantic Caching
- GPU-aware Scheduling
- ML-driven Routing Policies
- CI/CD Pipelines
- Advanced Benchmarking

---

## ✍️ Author

Shubham Dewangan
