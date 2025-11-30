# 🚀 Deployment Guide

## Live Demo URL

**Production:** (Ready to deploy to Railway/Heroku)

---

## Deployment Options

### Option 1: Railway (Recommended - Easiest) ⭐

Railway adalah platform deployment tercepat dengan GitHub integration.

#### Step 1: Prepare GitHub Repository

```bash
# Initialize git repo
git init
git add .
git commit -m "Initial commit: Kasir Digital API v2.0"

# Push ke GitHub
git remote add origin https://github.com/yourusername/kasir-digital-api.git
git push -u origin main
```

#### Step 2: Deploy to Railway

1. Visit https://railway.app
2. Login dengan GitHub account
3. Click "New Project" → "Deploy from GitHub"
4. Select `kasir-digital-api` repository
5. Railway akan auto-detect Python + install dependencies
6. API akan live dalam 2-3 menit!

#### Step 3: Get Production URL

```
https://your-app-name.railway.app
```

**Test Production API:**

```bash
# Register
curl -X POST https://your-app-name.railway.app/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"yusuf","password":"password123"}'

# Login
curl -X POST https://your-app-name.railway.app/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"yusuf","password":"password123"}'
```

---

### Option 2: Heroku

#### Step 1: Install Heroku CLI

```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

#### Step 2: Deploy

```bash
# Login
heroku login

# Create app
heroku create your-app-name

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

**Production URL:**
```
https://your-app-name.herokuapp.com
```

---

### Option 3: Docker (Advanced)

#### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app"]
```

#### Create docker-compose.yml

```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
```

#### Deploy

```bash
# Build image
docker build -t kasir-digital-api .

# Run container
docker run -p 5000:5000 kasir-digital-api

# Push ke Docker Hub
docker push yourusername/kasir-digital-api
```

---

## Environment Variables

Create `.env` file untuk production:

```env
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost/kasir_digital
DEBUG=False
```

Dalam `app.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

app.config['ENV'] = os.getenv('FLASK_ENV', 'development')
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
```

---

## Monitoring & Logging

### Application Logs

```bash
# View logs (Railway)
railway logs

# View logs (Heroku)
heroku logs --tail

# View logs (Local)
tail -f logs/app.log
```

### Health Check Endpoint

Add untuk monitoring:

```python
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }), 200
```

### Uptime Monitoring

Setup uptime monitoring dengan free tools:
- Uptime Robot: https://uptimerobot.com
- Pingdom: https://www.pingdom.com
- Synthetic Monitoring: https://newrelic.com

---

## Performance Optimization

### 1. Enable Caching

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/produk', methods=['GET'])
@cache.cached(timeout=300)  # Cache for 5 minutes
@token_required
def get_produk():
    # ...
```

### 2. Add Compression

```python
from flask_compress import Compress

Compress(app)
```

### 3. Use CDN for Static Files

```
# Configure CloudFront / Cloudflare
```

### 4. Database Optimization

Migrate from JSON ke PostgreSQL:

```python
# Migration script
import psycopg2

conn = psycopg2.connect("dbname=kasir_digital user=postgres")
# ... migrate data
```

---

## Security Checklist

- ✅ Change SECRET_KEY in production
- ✅ Enable HTTPS (automatic di Railway/Heroku)
- ✅ Add CORS headers
- ✅ Setup HTTPS redirect
- ✅ Add rate limiting
- ✅ Setup WAF (Web Application Firewall)

```python
from flask_limiter import Limiter

limiter = Limiter(
    app=app,
    key_func=lambda: request.remote_addr,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/transaksi', methods=['POST'])
@limiter.limit("10 per minute")
def buat_transaksi():
    # ...
```

---

## Database Migration (SQLite → PostgreSQL)

### Create PostgreSQL Database

```bash
# Using Railway's PostgreSQL plugin
# Or local: createdb kasir_digital
```

### Update Connection String

```python
import os

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://user:password@localhost/kasir_digital'
)

# Use SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)
```

---

## Scaling for Production

### Horizontal Scaling

```bash
# Railway: Add more replicas
# Heroku: Scale dynos
heroku ps:scale web=3
```

### Load Balancing

```
nginx
├── API Instance 1
├── API Instance 2
└── API Instance 3
```

### Database Replication

```
Primary PostgreSQL
├── Read Replica 1
└── Read Replica 2
```

---

## Backup & Disaster Recovery

### Automated Backups

```bash
# Railway PostgreSQL automatic backups
# Heroku: heroku backups:capture

# Manual backup
pg_dump kasir_digital > backup.sql

# Restore
psql kasir_digital < backup.sql
```

### Data Export

```python
# Export to CSV
import csv
import json

with open('transaksi_backup.csv', 'w') as f:
    writer = csv.writer(f)
    for transaksi in db.get_semua_transaksi():
        writer.writerow([...])
```

---

## Custom Domain

### Add Custom Domain

```bash
# Railway
railway domain add yourdomain.com

# Heroku
heroku domains:add yourdomain.com
```

### Setup DNS

```
CNAME: yourdomain.com → your-app-name.railway.app
```

---

## CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Railway

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy
        run: |
          railway up
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|---|---|
| Import errors | Check `requirements.txt` |
| Database not connecting | Verify DATABASE_URL env var |
| Port issues | Check PORT env variable |
| Memory errors | Reduce dataset size or upgrade plan |
| Timeout errors | Increase timeout, optimize queries |

### Debug Mode

```python
app.run(debug=False)  # Always False in production!

# But enable logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

---

## Post-Deployment Checklist

- ✅ Test all endpoints on production
- ✅ Verify authentication works
- ✅ Check API response times
- ✅ Monitor error logs
- ✅ Setup uptime monitoring
- ✅ Enable automatic backups
- ✅ Configure custom domain
- ✅ Add HTTPS certificate
- ✅ Setup rate limiting
- ✅ Document API for users

---

## Costs

| Service | Free Tier | Pricing |
|---|---|---|
| Railway | 5 GB bandwidth/month | $5/month |
| Heroku | Deprecated | $7/month (basic dyno) |
| AWS | 12 months free | Pay-as-you-go |
| Google Cloud | $300 credits | Pay-as-you-go |

---

**Ready to Deploy! 🚀**

Next step: Push ke GitHub dan deploy ke Railway dalam 5 menit!
