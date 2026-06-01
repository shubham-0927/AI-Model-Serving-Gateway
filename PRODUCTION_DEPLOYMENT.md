# Production Deployment Guide

## Pre-Deployment Checklist

### 1. Environment Variables
Before deploying, you **MUST** create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Update the following critical variables in `.env`:

```
# CRITICAL: Change these values immediately
DATABASE_URL=postgresql://postgres:CHANGE_ME_SECURE_PASSWORD@postgres:5432/aigateway
SECRET_KEY=CHANGE_ME_TO_SECURE_RANDOM_STRING
POSTGRES_PASSWORD=CHANGE_ME_SECURE_PASSWORD
GRAFANA_PASSWORD=CHANGE_ME_SECURE_PASSWORD
```

### 2. Generate Secure Values

**Generate a secure SECRET_KEY:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Generate a secure database password:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(24))"
```

### 3. Database URL Format

The `DATABASE_URL` should follow this format:
```
postgresql://USERNAME:PASSWORD@HOST:PORT/DATABASE_NAME
```

Example for Docker deployment:
```
postgresql://postgres:your_secure_password@postgres:5432/aigateway
```

## Production Hardening

### 1. Removed Hardcoded Values
✅ Removed hardcoded PostgreSQL credentials (was: postgres:postgres)
✅ Removed hardcoded SECRET_KEY fallback (was: "supersecret")
✅ Removed hardcoded Redis defaults
✅ Added environment variable validation in `app/core/config.py`

### 2. Security Measures

- **SECRET_KEY**: Now required and must differ from default values
- **DATABASE_URL**: Required environment variable
- **POSTGRES_PASSWORD**: Must be explicitly set
- **All defaults removed**: Production requires explicit configuration

### 3. Docker Compose Updates

- Environment variables now use `${VAR_NAME}` syntax
- Required variables marked with `${VAR:?error message}`
- Optional variables with sensible defaults

## Deployment Steps

### 1. Prepare Environment
```bash
# Copy and configure environment file
cp .env.example .env
# Edit .env with your production values
nano .env
```

### 2. Build Docker Images
```bash
docker-compose build
```

### 3. Start Services
```bash
docker-compose up -d
```

### 4. Verify Deployment
```bash
# Check health endpoint
curl http://localhost:8000/health

# Check database connection
curl http://localhost:8000/health/db

# Check metrics
curl http://localhost:8000/metrics
```

### 5. Monitor Services
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (login: admin / your_grafana_password)
- Jaeger: http://localhost:16686

## Important Security Notes

1. **Never commit `.env` file** - It's in `.gitignore`
2. **Use strong passwords** - At least 24 characters recommended
3. **Rotate secrets regularly** - Update SECRET_KEY periodically
4. **Use secrets management** - Consider using HashiCorp Vault in production
5. **Enable HTTPS** - Configure SSL/TLS in nginx
6. **Set ALLOWED_ORIGINS** - Configure CORS appropriately

## Database Backup

Before production deployment:

```bash
# Backup database
pg_dump -U postgres aigateway > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore database
psql -U postgres aigateway < backup_file.sql
```

## Scaling Considerations

For production deployment at scale:

1. **Uvicorn Workers**: Adjust `WORKERS` environment variable
2. **Redis Persistence**: Enable AOF/RDB in production
3. **Database Replication**: Set up PostgreSQL streaming replication
4. **Load Balancing**: Use multiple API instances behind nginx
5. **Monitoring**: Ensure Prometheus/Grafana are accessible

## Troubleshooting

### Issue: "DATABASE_URL environment variable is required"
**Solution**: Ensure `.env` file exists and `DATABASE_URL` is set

### Issue: "SECRET_KEY environment variable is required"
**Solution**: Generate a secure key: `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`

### Issue: PostgreSQL connection failed
**Solution**: Verify `POSTGRES_PASSWORD` matches in `.env` and docker-compose.yml

### Issue: Container won't start
**Solution**: Check logs: `docker-compose logs -f api`

## Additional Resources

- [FastAPI Production Deployment](https://fastapi.tiangolo.com/deployment/concepts/)
- [PostgreSQL Security](https://www.postgresql.org/docs/current/sql-syntax.html)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
