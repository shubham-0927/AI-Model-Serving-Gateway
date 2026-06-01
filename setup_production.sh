#!/bin/bash
# Setup script for production deployment
# Usage: bash setup_production.sh

set -e

echo "🚀 AI Gateway Production Setup Script"
echo "======================================"

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "ℹ️  Creating .env from .env.example..."
    cp .env.example .env
    echo "✅ .env created. Please edit it with your configuration."
else
    echo "✅ .env file exists"
fi

# Validate required environment variables
required_vars=("DATABASE_URL" "SECRET_KEY" "POSTGRES_PASSWORD")
missing_vars=()

echo ""
echo "Checking required environment variables..."

for var in "${required_vars[@]}"; do
    if grep -q "^${var}=" .env; then
        value=$(grep "^${var}=" .env | cut -d'=' -f2-)
        if [[ $value == *"CHANGE_ME"* ]] || [[ -z "$value" ]]; then
            missing_vars+=("$var")
            echo "⚠️  $var is not configured (contains placeholder)"
        else
            echo "✅ $var is configured"
        fi
    else
        missing_vars+=("$var")
        echo "❌ $var is missing from .env"
    fi
done

if [ ${#missing_vars[@]} -gt 0 ]; then
    echo ""
    echo "❌ Please configure the following variables in .env:"
    printf '   - %s\n' "${missing_vars[@]}"
    exit 1
fi

echo ""
echo "✅ All required variables are configured!"

# Generate example secure values
echo ""
echo "💡 Secure value generators:"
echo "   SECRET_KEY: $(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')"
echo "   Password: $(python3 -c 'import secrets; print(secrets.token_urlsafe(24))')"

echo ""
echo "🐳 Docker setup complete!"
echo ""
echo "Next steps:"
echo "1. Review and edit .env file with your production values"
echo "2. Run: docker-compose build"
echo "3. Run: docker-compose up -d"
echo "4. Verify: curl http://localhost:8000/health"

echo ""
echo "📚 See PRODUCTION_DEPLOYMENT.md for detailed instructions"
