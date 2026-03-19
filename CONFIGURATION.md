# 🔧 Configuration & Deployment Guide

## Local Setup

### Windows
1. Install Python 3.8+ from [python.org](https://python.org)
2. Run `setup.bat` in the project directory
3. Copy `templates/index.html` to the `templates` folder
4. Run `python app.py`
5. Open http://localhost:5000

### macOS/Linux
1. Install Python 3.8+: `brew install python3` (macOS) or `apt install python3` (Linux)
2. Run `bash setup.sh`
3. Copy `templates/index.html` to the `templates` folder
4. Run `python app.py`
5. Open http://localhost:5000

## Docker Deployment

### Quick Start
```bash
docker-compose up --build
```

### Manual Docker Build
```bash
docker build -t instagram-checker .
docker run -p 5000:5000 -v $(pwd)/hits.txt:/app/hits.txt instagram-checker
```

## Environment Variables

Create a `.env` file:

```env
# Flask
FLASK_ENV=production
FLASK_APP=app.py
FLASK_DEBUG=0

# Instagram Proxies (comma-separated)
INSTAGRAM_PROXIES=http://proxy1:8080,http://proxy2:8080

# VPN Proxies (comma-separated)
INSTAGRAM_VPN_PROXIES=http://vpn1:8080,http://vpn2:8080

# Settings
CHECK_DELAY=1.0
USE_PROXIES=false
USE_VPN=false
LOG_HITS=true
```

Load with:
```bash
python -u app.py
```

## Proxy Configuration

### File-based (proxies.txt)
```
http://proxy1.com:8080
http://proxy2.com:8080
socks5://proxy3.com:1080
socks5://user:pass@proxy4.com:1080
```

### Environment Variables
```bash
export INSTAGRAM_PROXIES="http://p1:8080,http://p2:8080"
export INSTAGRAM_VPN_PROXIES="http://vpn1:8080"
python app.py
```

### API (Runtime)
POST to `/api/proxies`:
```json
{
  "proxy_url": "http://proxy:8080",
  "is_vpn": false
}
```

## Settings Configuration

Edit `settings.json` directly or via UI:

```json
{
  "check_delay": 1.0,           // Delay between checks (seconds)
  "use_proxies": false,          // Enable proxy rotation
  "use_vpn": false,              // Route through VPN
  "randomize_ua": true,          // Random user agents
  "max_accounts": 5,             // Maximum test accounts
  "rate_limit": 2,               // Rate limit (seconds)
  "log_hits": true,              // Save hits to file
  "auto_save_interval": 30       // Auto-save interval (seconds)
}
```

## Account Management

### Adding Accounts
Via Web UI: Click **"+ Add"** button

Via API:
```bash
curl -X POST http://localhost:5000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{"username": "test_account", "password": "password123"}'
```

### Bulk Import
Programmatically in Python:
```python
import requests

accounts = [
    ("account1", "password1"),
    ("account2", "password2"),
    ("account3", "password3"),
]

for username, password in accounts:
    requests.post(
        "http://localhost:5000/api/accounts",
        json={"username": username, "password": password}
    )
```

## Performance Tuning

### For Speed (Higher Risk)
```json
{
  "check_delay": 0.5,
  "use_proxies": true,
  "rate_limit": 1,
  "max_accounts": 5
}
```

### For Safety (Lower Risk)
```json
{
  "check_delay": 3.0,
  "use_proxies": true,
  "use_vpn": true,
  "rate_limit": 5,
  "max_accounts": 2
}
```

### Balanced
```json
{
  "check_delay": 1.5,
  "use_proxies": true,
  "rate_limit": 2,
  "max_accounts": 3
}
```

## Advanced Usage

### CLI Mode (Alternative to Web UI)

Create `cli_checker.py`:
```python
import requests
import json

BASE_URL = "http://localhost:5000/api"

# Add accounts
for user, pwd in [("acc1", "pass1"), ("acc2", "pass2")]:
    requests.post(f"{BASE_URL}/accounts", 
                  json={"username": user, "password": password})

# Start checking
usernames = ["cool", "awesome", "rad", "sick", "fire"]
accounts = requests.get(f"{BASE_URL}/accounts").json()
account_ids = list(accounts.keys())

requests.post(f"{BASE_URL}/checker/check",
              json={"usernames": usernames, "account_ids": account_ids})

# Wait and get results
import time
while True:
    status = requests.get(f"{BASE_URL}/checker/status").json()
    print(f"Progress: {status['progress']}%")
    if not status['active']:
        break
    time.sleep(1)

# Export results
hits = requests.get(f"{BASE_URL}/hits").json()
print("Available usernames:")
for hit in hits:
    print(f"  - {hit['username']}")
```

Run with: `python cli_checker.py`

### Headless Mode (No UI)

Remove Flask static/template serving:
```python
# In app.py, comment out:
# @app.route('/')
# def index():
#     return render_template('index.html')
```

Use via API only (CLI, scripts, other apps).

### Integration with Other Tools

#### With Zapier/IFTTT
Post to `/api/checker/check` when triggered:
```python
webhook_payload = {
    "usernames": ["list", "of", "usernames"],
    "account_ids": ["account_id_1", "account_id_2"]
}
```

#### With Discord Bot
Post hits to Discord webhook:
```python
import discord

webhook = discord.SyncWebhook.from_url(WEBHOOK_URL)

# When hit is added:
webhook.send(f"✅ Found available username: **cool.username**")
```

## Monitoring & Analytics

### Hit Statistics
```bash
# Count total hits
wc -l hits.txt

# View recent hits
tail -20 hits.txt

# Parse JSON
cat hits.txt | python -m json.tool
```

### Performance Metrics

Add to `app.py`:
```python
from datetime import datetime

@app.route('/api/stats', methods=['GET'])
def get_stats():
    hits = hit_tracker.get_hits()
    accounts = account_manager.get_all_accounts()
    
    total_checks = sum(a.get('checks_count', 0) for a in accounts.values())
    
    return jsonify({
        "total_hits": len(hits),
        "total_checks": total_checks,
        "hit_rate": (len(hits) / total_checks * 100) if total_checks > 0 else 0,
        "active_accounts": sum(1 for a in accounts.values() if a['status'] == 'online'),
        "total_accounts": len(accounts)
    })
```

## Security Best Practices

### 1. Use Firewall
```bash
sudo ufw allow 5000/tcp
```

### 2. Reverse Proxy with Nginx
```nginx
server {
    listen 80;
    server_name instagram-checker.local;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
    }
}
```

### 3. Basic Auth
```python
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    return username == "admin" and password == "secure_password"

@app.route('/api/accounts', methods=['GET'])
@auth.login_required
def get_accounts():
    # ...
```

### 4. HTTPS/SSL
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# In app.py:
app.run(ssl_context=('cert.pem', 'key.pem'))
```

### 5. Credential Encryption
```python
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

def encrypt_password(password):
    return cipher.encrypt(password.encode()).decode()

def decrypt_password(encrypted):
    return cipher.decrypt(encrypted.encode()).decode()
```

## Troubleshooting

### Port Already in Use
```bash
# Find what's using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>

# Or use different port
python app.py --port 5001
```

### ModuleNotFoundError
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Or use virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Instagram Changes API
Monitor for updates:
- [instagrapi GitHub Issues](https://github.com/subzeroid/instagrapi/issues)
- Instagram security updates
- API changes

### Accounts Getting Banned
- Increase check delay
- Use more accounts (distribute load)
- Use proxies/VPN
- Space out checks over time
- Use proper user agents

## Backup & Migration

### Backup Everything
```bash
# Create backup
tar -czf instagram-checker-backup.tar.gz \
  hits.txt accounts_state.json settings.json proxies.txt

# Restore
tar -xzf instagram-checker-backup.tar.gz
```

### Export Hits
```bash
curl http://localhost:5000/api/hits/export -o hits.txt
```

## Performance Limits

| Feature | Limit | Notes |
|---------|-------|-------|
| Test Accounts | 5 | Per instance |
| Concurrent Checks | Unlimited | Rate limited by delay |
| Usernames per Check | Unlimited | Memory dependent |
| Check Delay | 0.1s min | Higher = safer |
| Hits per Hour | ~3600 | Depends on delay |

## Scaling

### Horizontal Scaling
Run multiple instances behind load balancer:
```bash
python app.py --port 5001 &
python app.py --port 5002 &
python app.py --port 5003 &
```

### Persistent Storage
Use database instead of JSON:
- PostgreSQL
- MongoDB
- Redis

### Queue System
Use Celery for background jobs:
```python
from celery import Celery

celery = Celery(app.name)
```

## Support & Issues

- GitHub Issues: [instagrapi/issues](https://github.com/subzeroid/instagrapi/issues)
- Documentation: Check README.md
- Community: Forums, Discord, etc.

---

**Last Updated**: 2024-01-15
