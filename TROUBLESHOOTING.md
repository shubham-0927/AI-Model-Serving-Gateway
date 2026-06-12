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

