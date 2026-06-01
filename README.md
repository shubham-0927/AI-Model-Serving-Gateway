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

## 🛠️ Troubleshooting

### ❌ "docker-compose: command not found"

**Solution:** You have Docker v1. Install Docker Compose standalone:

```bash
# macOS
brew install docker-compose

# Linux
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

Or use the newer syntax:

```bash
docker compose up --build  # instead of docker-compose
```

---

### ❌ "postgres: DATABASE_URL must be set"

**Cause:** Environment variables not loaded

**Solution:**

```bash
# Verify .env exists
ls -la .env

# Verify .env has DATABASE_URL
cat .env | grep DATABASE_URL

# Rebuild and restart
docker compose down
docker compose up --build

# OR if using docker-compose (older):
docker-compose down
docker-compose up --build
```

---

### ❌ "postgres: POSTGRES_PASSWORD is not set"

**Cause:** Missing `.env` file

**Solution:**

```bash
# Create from example
cp .env.example .env

# Edit if needed
nano .env  # or use your editor

# Restart
docker compose down
docker compose up --build
```

---

### ❌ "connection refused" to API

**Cause:** Services not ready or failed to start

**Solution:**

```bash
# Check service status
docker compose ps

# View logs to see errors
docker compose logs api -f

# Wait 30 seconds for initialization, then retry
# Services startup order:
# 1. postgres (30s)
# 2. redis (10s)
# 3. api (20s)

# Restart problematic service
docker compose restart api
```

---

### ❌ "curl: (7) Failed to connect to localhost port 8000"

**Cause:** API not running or port not exposed

**Solution:**

```bash
# Check if nginx is running and proxying correctly
docker compose ps

# Verify nginx configuration
curl -I http://localhost/health

# If using direct port:
curl -I http://localhost:8000/health

# Check docker networking
docker compose exec api curl -I http://localhost:8000/health

# View nginx logs
docker compose logs nginx
```

---

### ❌ "ERROR: Secret key is required and must be changed from default"

**Cause:** `SECRET_KEY` not set in `.env` or using insecure default

**Solution:**

```bash
# Generate a new secure key
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Add to .env
echo "SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')" >> .env

# Restart
docker compose down
docker compose up --build
```

---

### ❌ "Permission denied: /var/lib/postgresql/data"

**Cause:** Docker permission issue

**Solution:**

```bash
# Stop services
docker compose down

# Remove volume and recreate
docker volume rm ai-gateway_postgres_data 2>/dev/null || true

# Restart with fresh database
docker compose up --build
```

---

### ❌ Prometheus not scraping metrics

**Cause:** API or Prometheus misconfiguration

**Solution:**

```bash
# Check API metrics endpoint
curl http://localhost/metrics | head -20

# Check Prometheus targets
curl -s http://localhost:9090/api/v1/targets | jq .

# View prometheus logs
docker compose logs prometheus

# Check if prometheus.yml is correct
docker compose exec prometheus cat /etc/prometheus/prometheus.yml
```

---

### ❌ Cannot create API key - "user_id not found"

**Cause:** User not registered or ID mismatch

**Solution:**

```bash
# Register user first
curl -X POST http://localhost/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'

# Copy the returned user_id

# Then create key with correct user_id
curl -X POST http://localhost/keys/create \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "PASTE_USER_ID_HERE",
    "name": "my-key"
  }'
```

---

### ❌ "FATAL: database 'aigateway' does not exist"

**Cause:** Database not initialized

**Solution:**

```bash
# Postgres initializes on first run - wait 60 seconds

# Check if postgres is healthy
docker compose exec postgres pg_isready

# Manual initialization (if needed)
docker compose exec postgres psql -U postgres -c "CREATE DATABASE aigateway;"

# Restart API
docker compose restart api
```

---

### ❌ Celery worker not processing tasks

**Cause:** Worker crashed or not connected to Redis

**Solution:**

```bash
# Check worker status
docker compose logs worker -f

# Verify Redis connection
docker compose exec redis redis-cli ping
# Should return: PONG

# Restart worker
docker compose restart worker

# Check Celery events
docker compose exec worker celery -A app.workers.celery_app events
```

---

### ❌ "Out of memory" errors

**Cause:** Docker resource limits

**Solution:**

```bash
# Check memory usage
docker stats

# Increase Docker resources:
# Docker Desktop: Settings → Resources → Memory (set to 6GB+)
# Linux: Adjust container memory in docker-compose.yml

# Stop unused services
docker compose down

# Rebuild
docker compose up --build
```

---

### ❌ Port already in use

**Cause:** Service already running on that port

**Solution:**

```bash
# Find what's using port 3000 (example)
lsof -i :3000  # macOS/Linux
netstat -ano | findstr :3000  # Windows

# Kill process or change docker-compose port mapping
# Edit docker-compose.yml:
#   ports:
#     - "3001:3000"  # Use 3001 instead

# Restart
docker compose up --build
```

---

### 🐛 Debug Mode

Enable verbose logging for troubleshooting:

```bash
# In .env
DEBUG=true
APP_ENV=development

# Restart
docker compose down
docker compose up --build

# View detailed logs
docker compose logs -f api
```

---

### 📞 Getting Help

1. **Check logs first:**
   ```bash
   docker compose logs <service-name> -f
   ```

2. **Check status:**
   ```bash
   docker compose ps
   docker stats
   ```

3. **Check connectivity:**
   ```bash
   curl -v http://localhost/health
   docker compose exec api python3 -c "from app.db.session import get_db; print('DB OK')"
   ```

4. **Review documentation:**
   - QUICK_REFERENCE.md - Common commands
   - START_HERE.md - Testing guide
   - GRAFANA_SETUP.md - Dashboard setup

---



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

## 📝 Recent Changes & Updates

### ✨ New for First-Time Users (This Release)

**Complete Setup Guide Added**

1. ✅ **`.env.example` file** - Template with all configuration options
2. ✅ **Quick Start Guide** - 5-minute setup walkthrough
3. ✅ **Prerequisites Checklist** - All system requirements listed
4. ✅ **Environment Variables Documented** - All config options explained with examples
5. ✅ **Step-by-Step Setup** - From cloning to first API request
6. ✅ **Comprehensive Troubleshooting** - 15+ common issues and solutions
7. ✅ **API Key Creation Guide** - First-time user registration workflow
8. ✅ **Dashboard Access Guide** - Grafana, Prometheus, Jaeger URLs

### Key Things First-Time Users Must Know

- **`.env` file is REQUIRED** - Copy `.env.example` to `.env` before running
- **Change `SECRET_KEY` in production** - Generate new key: `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`
- **Docker/Docker Compose required** - The project runs entirely in containers
- **Initial setup takes ~2 minutes** - Services initialize automatically
- **Test data available** - Run `run_quick_start.sh` to start testing

### Files You Should Know

| File | Purpose |
|------|---------|
| `.env` | Your configuration (create from `.env.example`) |
| `.env.example` | Template with all available options and explanations |
| `docker-compose.yml` | Service definitions and configuration |
| `requirements.txt` | Python dependencies |
| `START_HERE.md` | Testing & demo guide |
| `QUICK_REFERENCE.md` | Common commands & quick help |
| `README_TEST_SUITE.md` | Full test suite documentation |

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

![Visitors](https://visitorbadge.io)
![Views](https://komarev.com)



## ✍️ Author

Shubham Dewangan
