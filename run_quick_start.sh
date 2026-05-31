#!/bin/bash
# Quick Start Script - Run the complete test suite in one command

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "==============================================="
echo "  AI GATEWAY - QUICK START TEST SUITE"
echo "==============================================="
echo ""

# Check if docker compose is running
echo "[1/5] Checking Docker containers..."
if ! docker compose ps 2>/dev/null | grep -q "ai_gateway"; then
    echo "✗ Docker containers not running!"
    echo "Please run: docker compose up --build"
    exit 1
fi
echo "✓ Docker containers are running"
echo ""

# Wait for API to be ready
echo "[2/5] Waiting for API to be ready..."
max_attempts=30
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if curl -s http://localhost/health > /dev/null 2>&1; then
        echo "✓ API is ready"
        break
    fi
    attempt=$((attempt + 1))
    if [ $attempt -lt $max_attempts ]; then
        echo "  Waiting... (attempt $attempt/$max_attempts)"
        sleep 2
    fi
done

if [ $attempt -eq $max_attempts ]; then
    echo "✗ API is not responding"
    exit 1
fi
echo ""

# Run test setup
echo "[3/5] Setting up test environment..."
if python3 test_setup.py; then
    echo "✓ Test setup complete"
else
    echo "✗ Test setup failed"
    exit 1
fi
echo ""

# Show pre-test information
echo "[4/5] Preparing to start tests..."
echo ""
echo "This will run a 60-minute comprehensive test suite consisting of:"
echo "  • Load Test (20 min) - Steady user traffic"
echo "  • Resilience Test (20 min) - Failover and recovery"
echo "  • Stress Test (20 min) - High load conditions"
echo ""

# Show monitoring dashboard URLs
echo "[5/5] Opening monitoring dashboards..."
echo ""
echo "Open these URLs in your browser to monitor tests in real-time:"
echo "  1. Prometheus:  http://localhost:9090"
echo "  2. Grafana:     http://localhost:3000  (admin/admin)"
echo "  3. Jaeger:      http://localhost:16686"
echo ""
echo "Press ENTER to start the 60-minute test suite..."
read -r

# Run the main test suite
echo ""
echo "Starting tests at $(date)"
echo "==============================================="
python3 run_tests.py

echo ""
echo "Test suite completed at $(date)"
echo "==============================================="
echo ""
echo "Next steps:"
echo "  1. Review dashboards for trends and insights"
echo "  2. Check logs: docker logs ai_gateway_api -f"
echo "  3. Query database: docker compose exec postgres psql -U postgres -d aigateway"
