# 📸 Instagram Username Checker - Flask Edition
## Complete Project Index & Setup Guide

---

## 📦 PROJECT CONTENTS

### Core Application Files
- **`app.py`** - Flask backend with all logic (800+ lines)
  - Account management (add/remove/login/logout)
  - Multi-account pooling system
  - Username checking with instagrapi
  - Hit tracking and management
  - Settings management
  - Proxy/VPN support
  - 2FA detection

- **`templates/index.html`** - Frontend UI (1000+ lines)
  - Dark neon cyberpunk aesthetic
  - Real-time progress tracking
  - Account status panel with login controls
  - Username generators (random, pattern, wordlist)
  - Settings modal
  - Hits display and export
  - Fully responsive design

### Configuration & Deployment
- **`requirements.txt`** - Python dependencies
  - Flask 2.3.3
  - instagrapi 2.0.0
  - Flask-CORS for API
  - requests for proxies

- **`Dockerfile`** - Container config
- **`docker-compose.yml`** - Orchestration
- **`setup.sh`** - Linux/Mac auto-setup
- **`setup.bat`** - Windows auto-setup

### Documentation
- **`README.md`** - Complete documentation (300+ lines)
  - Features overview
  - Installation guide
  - Usage instructions
  - API documentation
  - Troubleshooting guide

- **`CONFIGURATION.md`** - Advanced configuration (350+ lines)
  - Environment variables
  - Proxy setup
  - Performance tuning
  - Docker deployment
  - Security best practices
  - Scaling strategies

- **`QUICK_START.md`** - 30-second setup guide
  - Quick reference
  - File listing
  - Common workflows
  - Troubleshooting table

---

## 🚀 QUICK START (Copy & Paste)

### Windows
```batch
setup.bat
python app.py
```
Then: **http://localhost:5000**

### macOS/Linux
```bash
bash setup.sh
python app.py
```
Then: **http://localhost:5000**

### Docker
```bash
docker-compose up --build
```
Then: **http://localhost:5000**

---

## 📋 FILE STRUCTURE AFTER SETUP

```
instagram-checker/
├── app.py                          # Flask app
├── requirements.txt                # Dependencies
├── Dockerfile                      # Docker config
├── docker-compose.yml              # Docker Compose
├── setup.sh                        # Linux/Mac setup
├── setup.bat                       # Windows setup
├── README.md                       # Full docs
├── CONFIGURATION.md                # Advanced config
├── QUICK_START.md                  # Quick ref
├── templates/
│   └── index.html                 # Web UI (COPY HERE)
├── settings.json                  # Auto-created
├── accounts_state.json            # Auto-created
├── hits.txt                       # Auto-created
└── proxies.txt                    # Auto-created
```

---

## ✨ CORE FEATURES

### Account Management
✅ Add up to 5 Instagram test accounts
✅ Login/logout with 2FA support
✅ View account status (online/offline)
✅ Track check count per account
✅ Remove accounts from web panel
✅ Credentials saved locally

### Username Generation
🎲 **Random Generator**
  - Generate A-Z, a-z, 0-9, `.`, `_`
  - Configurable length (1-10 chars)
  - Batch generation

📝 **Pattern Generator**
  - Create variations: `base_123`, `base.456`
  - Wildcard variations
  - Auto-combine separators

📖 **Wordlist Loader**
  - Load from text files
  - One username per line
  - Unlimited wordlist size

### Checking & Results
🔍 **Real-time Checking**
  - Live progress bar
  - Current/total count
  - Percentage indicator
  - Account rotation

✅ **Hit Tracking**
  - Auto-save to `hits.txt`
  - JSON format with timestamps
  - Metadata tracking
  - Remove individual hits

📊 **Statistics**
  - Available count
  - Taken count
  - Error count
  - Success rate

### Advanced Features
🌐 **Proxy Support**
  - HTTP/HTTPS proxies
  - SOCKS5 support
  - VPN proxy routing
  - Per-check rotation

🎭 **Device Spoofing**
  - Random user agents
  - Multiple device profiles
  - Realistic Android signatures
  - Per-login randomization

⚙️ **Settings Panel**
  - Check delay (0.1s - 5s)
  - Rate limiting
  - Proxy enable/disable
  - VPN enable/disable
  - Hit logging toggle

---

## 🔐 SECURITY FEATURES

✓ 2FA Support
  - SMS verification
  - TOTP (authenticator app)
  - Challenge detection

✓ Proxy/VPN
  - Distribute requests
  - Hide IP address
  - Bypass detection

✓ Device Randomization
  - Rotate user agents
  - Multiple device profiles
  - Realistic signatures

✓ Account Rotation
  - Distribute checks
  - Avoid rate limiting
  - Reduce detection risk

---

## 🎨 UI/UX HIGHLIGHTS

**Dark Neon Aesthetic**
- Primary: Cyan (#00d4ff)
- Secondary: Hot Pink (#ff006e)
- Accent: Yellow (#ffbe0b)
- Success: Lime Green (#00ff88)
- Error: Red (#ff3333)

**Animations**
- Slide-up entrance (staggered)
- Smooth transitions (0.3s)
- Pulsing loading states
- Hover effects

**Layout**
- 3-panel responsive grid
- Accounts | Checker | Hits
- Mobile-optimized
- Custom scrollbars

**Interactions**
- Modal dialogs
- Tab switching
- Progress bar
- Status badges
- Checkboxes

---

## 📊 API ENDPOINTS

### Accounts
- `GET /api/accounts` - List all
- `POST /api/accounts` - Add account
- `DELETE /api/accounts/<id>` - Remove
- `POST /api/accounts/<id>/login` - Login
- `POST /api/accounts/<id>/logout` - Logout

### Checker
- `POST /api/checker/check` - Start checking
- `GET /api/checker/status` - Get progress
- `POST /api/checker/stop` - Stop checking

### Hits
- `GET /api/hits` - Get all hits
- `DELETE /api/hits/<username>` - Remove hit
- `GET /api/hits/export` - Export as file

### Generator
- `POST /api/generator/random` - Random generation
- `POST /api/generator/pattern` - Pattern generation
- `POST /api/generator/wordlist` - Load wordlist

### Settings
- `GET /api/settings` - Get settings
- `POST /api/settings` - Update settings

### Proxies
- `GET /api/proxies` - Get all proxies
- `POST /api/proxies` - Add proxy

---

## 🔧 INSTALLATION STEPS

### Step 1: Install Python
- Windows: [python.org](https://python.org)
- macOS: `brew install python3`
- Linux: `apt install python3`

### Step 2: Setup Project
```bash
# Clone/download project
cd instagram-checker

# Run setup script
bash setup.sh        # Linux/Mac
# OR
setup.bat           # Windows
```

### Step 3: Copy UI
Copy the HTML file to templates folder:
```bash
mkdir -p templates
cp templates_index.html templates/index.html
```

### Step 4: Run Application
```bash
python app.py
```

### Step 5: Access Web UI
Open browser: **http://localhost:5000**

---

## 📝 CONFIGURATION

### Environment Variables
```bash
FLASK_ENV=production
INSTAGRAM_PROXIES=http://p1:8080,http://p2:8080
INSTAGRAM_VPN_PROXIES=http://vpn1:8080
```

### Settings File (settings.json)
```json
{
  "check_delay": 1.0,
  "use_proxies": false,
  "use_vpn": false,
  "randomize_ua": true,
  "max_accounts": 5,
  "rate_limit": 2,
  "log_hits": true
}
```

### Proxy File (proxies.txt)
```
http://proxy1:8080
http://proxy2:8080
socks5://proxy3:1080
```

---

## 🐳 DOCKER DEPLOYMENT

### Quick Start
```bash
docker-compose up --build
```

### Manual
```bash
docker build -t checker .
docker run -p 5000:5000 checker
```

### Persistent Storage
```bash
docker run -p 5000:5000 \
  -v $(pwd)/hits.txt:/app/hits.txt \
  -v $(pwd)/settings.json:/app/settings.json \
  checker
```

---

## 📈 PERFORMANCE SPECS

| Setting | Speed | Safety |
|---------|-------|--------|
| Check Delay | 0.5s | ❌ Risky |
| Check Delay | 1.0s | ✅ Good |
| Check Delay | 2.0s | ✅✅ Safe |
| 1 Account | Fast | ❌ Risky |
| 3 Accounts | Good | ✅ Balanced |
| 5 Accounts | Risky | ❌ Unsafe |
| No Proxy | Fast | ❌ Detected |
| Proxy | Good | ✅ Safe |
| VPN Proxy | Slow | ✅✅ Safest |

### Optimal Configuration
- 2-3 accounts
- 1.5-2s delay
- HTTP proxies
- 50-100 usernames per batch

---

## 🚨 IMPORTANT NOTES

⚠️ **Use Throwaway Accounts Only**
- Instagram WILL ban accounts used for checking
- Never use main/important accounts
- Accept the risk

⚠️ **Terms of Service**
- May violate Instagram ToS
- Use responsibly
- Respect rate limits
- Don't abuse system

⚠️ **Credential Security**
- Stored in `accounts_state.json`
- Not encrypted by default
- Secure file permissions
- Don't share credentials

⚠️ **Detection Risk**
- Instagram has anti-bot detection
- Use proxies and delays
- Rotate accounts
- Space out checks
- Monitor account status

---

## 🐛 TROUBLESHOOTING

| Issue | Fix |
|-------|-----|
| Port 5000 in use | `lsof -i :5000` → `kill -9 PID` |
| Module not found | `pip install -r requirements.txt` |
| Login fails | Check credentials, enable 2FA |
| No accounts appear | Check `accounts_state.json` exists |
| Hits not saving | Enable "Log Hits" in settings |
| Slow checking | Reduce delay, use fewer accounts |
| Connection error | Check firewall, verify proxy config |

---

## 💡 COMMON WORKFLOWS

### Fast Hunting (Risky)
1. Add 5 accounts
2. Enable proxies
3. Set delay to 0.5s
4. Generate 1000+ usernames
5. Check all

### Safe Hunting (Recommended)
1. Add 2 accounts
2. Enable VPN proxies
3. Set delay to 2s
4. Generate 50-100 usernames
5. Check periodically

### Wordlist Processing
1. Load wordlist (1000+ words)
2. Login all accounts
3. Start checking
4. Export hits when done

---

## 📚 DOCUMENTATION

- **README.md** - Full documentation with examples
- **CONFIGURATION.md** - Advanced setup and scaling
- **QUICK_START.md** - 30-second reference
- **THIS FILE** - Complete index

---

## 🎯 NEXT STEPS

1. **Run setup script** - Initializes project
2. **Start app** - `python app.py`
3. **Add accounts** - Click "+ Add" button
4. **Generate usernames** - Use generators
5. **Start checking** - Click "Start Checking"
6. **View hits** - Check "✅ Hits" panel
7. **Export results** - Click "Export" button

---

## 📞 SUPPORT

- **Documentation**: See README.md
- **Advanced Help**: See CONFIGURATION.md
- **Quick Ref**: See QUICK_START.md
- **Errors**: Check browser console (F12)
- **Logs**: Check terminal output

---

## 📊 PROJECT STATS

- **Lines of Code**: 2500+
- **Python Code**: 800+ lines
- **HTML/CSS/JS**: 1000+ lines
- **Documentation**: 900+ lines
- **Features**: 20+
- **API Endpoints**: 15+

---

## ✅ WHAT'S INCLUDED

✓ Complete Flask backend
✓ Beautiful responsive UI
✓ Multi-account support
✓ 2FA handling
✓ Proxy/VPN support
✓ Hit tracking
✓ Settings management
✓ Docker support
✓ Full documentation
✓ Setup scripts (Windows, Linux, Mac)

---

## 🎓 LEARNING OUTCOMES

- Flask application architecture
- RESTful API design
- Real-time progress tracking
- Account pool management
- Proxy/VPN integration
- 2FA authentication
- Dark mode UI design
- Docker containerization

---

## 🚀 READY TO START?

### Quick Command
```bash
bash setup.sh && python app.py
```

### Then Open
```
http://localhost:5000
```

---

## 📄 File Checklist

After download, you should have:

- [ ] `app.py` - Flask backend
- [ ] `templates_index.html` - Copy to `templates/index.html`
- [ ] `requirements.txt` - Dependencies
- [ ] `README.md` - Full docs
- [ ] `CONFIGURATION.md` - Advanced setup
- [ ] `QUICK_START.md` - Quick ref
- [ ] `Dockerfile` - Docker config
- [ ] `docker-compose.yml` - Docker Compose
- [ ] `setup.sh` - Linux/Mac setup
- [ ] `setup.bat` - Windows setup
- [ ] `THIS_FILE` - Project index

---

**Made with ❤️ for username hunting enthusiasts**

**Questions?** Read the docs or check browser console for errors.

**Ready?** Run: `python app.py` 🚀

---

*Last Updated: 2024-01-15*
*Version: 1.0.0*
