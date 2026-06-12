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

## Live Demo

| Service | URL |
|----------|-----|
| Health Check | http://52.140.124.69/health |
| API Docs | http://52.140.124.69/docs |

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
## Deployment Infrastructure

The platform is deployed on an Azure VM using Docker Compose and consists of multiple infrastructure services working together.

### Services

| Service | Purpose |
|----------|----------|
| FastAPI API Gateway | Request routing and orchestration |
| Celery Workers | Background task processing |
| Celery Beat | Scheduled jobs |
| Redis | Shared state and caching |
| PostgreSQL | Persistent storage |
| RabbitMQ | Message broker |
| Prometheus | Metrics collection |
| Grafana | Observability dashboards |
| Jaeger | Distributed tracing |
| Nginx | Reverse proxy and ingress |

### Running Containers

![Docker Services](images/docker_services.png)

## Screenshots

### Grafana Observability Dashboard

Tracks:

- Provider latency
- Throughput
- Retry activity
- Failure rates
- Queue metrics
- Token consumption
- Provider health

![Grafana Dashboard](images/grafana_dashboard.png)

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

## ⚙️ Prerequisites

Before running the project, ensure you have:

- **Docker** (v20.10+) and **Docker Compose** (v1.29+)
  ```bash
  docker --version
  docker compose --version
  ```
- **Git** for cloning the repository
- **Python 3.12+** (if running outside Docker)
- **curl** or similar tool for testing APIs

### Check Prerequisites

```bash
# Verify Docker
docker run hello-world

# Verify Docker Compose
docker compose --version

# Verify Git
git --version
```

---

## 🚀 Quick Start (5 minutes)

### Step 1: Clone & Setup Environment

```bash
# Clone the repository
git clone <repository-url>
cd ai-gateway

# Copy environment configuration
cp .env.example .env

# IMPORTANT: Edit .env and change these in production:
# - SECRET_KEY (generate new: python3 -c "import secrets; print(secrets.token_urlsafe(32))")
# - POSTGRES_PASSWORD
# - GRAFANA_PASSWORD
```

### Step 2: Start Services

```bash
# Build and start all services
docker compose up --build

# Wait for services to initialize (~30 seconds)
# You should see: api, postgres, redis, prometheus, grafana, worker, beat all "running"
```

### Step 3: Verify Setup

```bash
# In a new terminal, check API health
curl http://localhost/health
# Expected: {"status":"ok"}

# Check database connection
curl http://localhost/health/db
# Expected: {"db":"connected"}

# Check Prometheus is scraping metrics
curl -s http://localhost:9090/api/v1/targets | grep "ai_gateway"
```

### Step 4: Create Your First API Key

```bash
# Register a new user
curl -X POST http://localhost/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePassword123!"
  }'
# Expected: {"user_id":"...","username":"testuser"}

# Generate an API key for the user
curl -X POST http://localhost/keys/create \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "YOUR_USER_ID_FROM_ABOVE",
    "name": "my-first-key"
  }'
# Expected: {"key_id":"...","key":"sk-..."}
# Save this key! You'll need it for API requests.
```

### Step 5: Try Your First Request

```bash
# Make a completions request with your API key
curl -X POST http://localhost/v1/completions \
  -H "Authorization: Bearer sk-YOUR_API_KEY_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is AI?",
    "strategy": "adaptive_routing",
    "stream": false
  }'
```

---

## 📊 Access Dashboards

Once services are running:

| Service | URL | Purpose |
|---------|-----|---------|
| **API Docs** | http://localhost/docs | Swagger documentation |
| **Grafana** | http://localhost:3000 | Dashboards (admin/admin) |
| **Prometheus** | http://localhost:9090 | Metrics browser |
| **Jaeger** | http://localhost:16686 | Distributed tracing |

---

## ▶️ Running the Project

### Start Services

```bash
docker compose up --build
```

### Stop Services

```bash
docker compose down
```

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f api
docker compose logs -f worker
docker compose logs -f postgres
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

## 📋 Environment Variables

All configuration is managed through `.env` file. See `.env.example` for all available options.

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:password@postgres:5432/aigateway` |
| `SECRET_KEY` | JWT signing key (change in production!) | `your-secret-key-123` |

### Important Docker Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `POSTGRES_USER` | `postgres` | Database username |
| `POSTGRES_PASSWORD` | `postgres` | Database password (change in production!) |
| `POSTGRES_DB` | `aigateway` | Database name |
| `GRAFANA_PASSWORD` | `admin` | Grafana admin password |

### Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_HOST` | `localhost` | Redis host (use `redis` in Docker) |
| `REDIS_PORT` | `6379` | Redis port |
| `APP_ENV` | `development` | Environment (development/staging/production) |
| `DEBUG` | `false` | Enable debug mode |
| `HOST` | `0.0.0.0` | Server bind address |
| `PORT` | `8000` | Server port |

---
## Common Issues

- Verify .env exists
- Verify Docker is running
- Verify all containers are healthy

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

## 📝 Recent Changes & Updates

<!-- ### ✨ New for First-Time Users (This Release)

**Complete Setup Guide Added**

1. ✅ **`.env.example` file** - Template with all configuration options
2. ✅ **Quick Start Guide** - 5-minute setup walkthrough
3. ✅ **Prerequisites Checklist** - All system requirements listed
4. ✅ **Environment Variables Documented** - All config options explained with examples
5. ✅ **Step-by-Step Setup** - From cloning to first API request
6. ✅ **Comprehensive Troubleshooting** - 15+ common issues and solutions
7. ✅ **API Key Creation Guide** - First-time user registration workflow
8. ✅ **Dashboard Access Guide** - Grafana, Prometheus, Jaeger URLs -->

### Key Things First-Time Users Must Know

- **`.env` file is REQUIRED** - Copy `.env.example` to `.env` before running
- **Change `SECRET_KEY` in production** - Generate new key: `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`
- **Docker/Docker Compose required** - The project runs entirely in containers
- **Initial setup takes ~2 minutes** - Services initialize automatically
- **Test data available** - Run `run_quick_start.sh` to start testing

### Files You Should Know

| File | Purpose |
|------|---------|
| [`.env`](./.env.example) | Create from `.env.example` and customize for your environment |
| [`.env.example`](./.env.example) | Template with all available options and explanations |
| [`docker-compose.yml`](./docker-compose.yml) | Service definitions and configuration |
| [`requirements.txt`](./requirements.txt) | Python dependencies |
| [`START_HERE.md`](./START_HERE.md) | Testing & demo guide |
| [`QUICK_REFERENCE.md`](./QUICK_REFERENCE.md) | Common commands & quick help |
| [`README_TEST_SUITE.md`](./README_TEST_SUITE.md) | Full test suite documentation |
| [`TROUBLESHOOTING.md`](./TROUBLESHOOTING.md) | Common issues, diagnostics, and recovery steps |

---

## 🎯 Next Steps for New Users

1. **Getting started?** → Read the **⚙️ Prerequisites** and **🚀 Quick Start** sections above
2. **Ready to test?** → Check out **START_HERE.md**
3. **Something not working?** → See **🛠️ Troubleshooting** section above
4. **Ready for production?** → See **PRODUCTION_DEPLOYMENT.md**
5. **Want nice dashboards?** → Check **GRAFANA_SETUP.md**

---

## Notes

Current providers are simulated for infrastructure and orchestration testing.
The architecture is designed to support real LLM providers later.

---



## ✍️ Author

Shubham Dewangan
