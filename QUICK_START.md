# 🚀 Quick Start Guide

## What You Got

A complete, production-ready Flask web application for checking Instagram username availability with a stunning dark neon UI.

## Files Included

```
📦 instagram-checker/
├── 🐍 app.py                    # Flask backend (main app)
├── 🎨 templates/
│   └── index.html              # Web UI (copy to templates/ folder)
├── 📋 requirements.txt          # Python dependencies
├── 📖 README.md                 # Full documentation
├── ⚙️  CONFIGURATION.md          # Advanced setup guide
├── 🐳 Dockerfile               # Docker container config
├── 🐳 docker-compose.yml       # Docker Compose (optional)
├── 🚀 setup.sh                 # Linux/Mac setup script
├── 🚀 setup.bat                # Windows setup script
└── 📄 THIS FILE                # Quick reference
```

## 30-Second Setup

### Windows
```batch
setup.bat
python app.py
```

### macOS/Linux
```bash
bash setup.sh
python app.py
```

Then open: **http://localhost:5000**

## Key Features

✅ **Multi-Account Support** - Up to 5 Instagram accounts simultaneously
✅ **Username Generators** - Random, pattern, and wordlist modes
✅ **Real-time Checking** - Live progress tracking
✅ **Hit Tracking** - Auto-save to `hits.txt`
✅ **Account Management** - Login/logout/remove accounts on the fly
✅ **2FA Support** - SMS and TOTP authentication
✅ **Proxy/VPN Support** - Rotate proxies per check
✅ **Dark Neon UI** - Cyberpunk aesthetic with animations

## First Steps

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the app**
   ```bash
   python app.py
   ```

3. **Open browser**
   ```
   http://localhost:5000
   ```

4. **Add test accounts**
   - Click "📱 Accounts" → "+ Add"
   - Enter Instagram credentials
   - Click "Login" to authenticate

5. **Generate usernames**
   - Switch to "Random", "Pattern", or "Wordlist" tab
   - Click generate button
   - Usernames appear in list

6. **Start checking**
   - Select accounts from dropdown
   - Click "Start Checking"
   - Watch progress in real-time
   - Available usernames appear in "✅ Hits" panel

7. **Export hits**
   - Click "Export" in Hits panel
   - Download `.txt` file

## Settings Panel

Click **⚙️ Settings** to configure:

| Setting | Default | What It Does |
|---------|---------|--------------|
| Check Delay | 1.0s | Wait between username checks |
| Rate Limit | 2s | Enforce rate limiting |
| Use Proxies | OFF | Rotate proxies |
| Use VPN | OFF | Route through VPN |
| Log Hits | ON | Save available usernames |

## API Endpoints

All requests to `http://localhost:5000/api/`

### Quick API Examples

**Add Account**
```bash
curl -X POST http://localhost:5000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{"username":"insta_user","password":"pass123"}'
```

**Get All Hits**
```bash
curl http://localhost:5000/api/hits | jq .
```

**Start Checking**
```bash
curl -X POST http://localhost:5000/api/checker/check \
  -H "Content-Type: application/json" \
  -d '{
    "usernames": ["cool", "awesome", "rad"],
    "account_ids": ["acc_id_1", "acc_id_2"]
  }'
```

**Get Progress**
```bash
curl http://localhost:5000/api/checker/status | jq .
```

## File Outputs

**hits.txt** - Available usernames in JSON format
```json
{"username": "cool", "timestamp": "2024-01-15T10:30:00", "metadata": {...}}
```

**settings.json** - Your preferences
```json
{"check_delay": 1.0, "use_proxies": false, ...}
```

**accounts_state.json** - Saved accounts
```json
{"abc123": {"username": "test_acc", "status": "online", ...}}
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 5000 in use | `lsof -i :5000` then `kill -9 <PID>` |
| Module not found | `pip install -r requirements.txt` |
| Login fails | Check username/password, enable 2FA if needed |
| No hits saved | Enable "Log Hits" in settings |
| Slow checking | Reduce delay, add more accounts, disable proxies |
| Can't find hits | Check hits.txt or export from UI |

## Docker Quick Start

```bash
docker-compose up --build
```

Then open: **http://localhost:5000**

Data persists in `hits.txt`, `settings.json`, etc.

## Common Workflows

### Fast Username Hunting (Risky)
1. Enable proxies in settings
2. Add 5 accounts
3. Set delay to 0.5 seconds
4. Generate 1000+ usernames
5. Check all at once

### Safe/Stealthy (Recommended)
1. Use 1-2 accounts
2. Set delay to 2-3 seconds
3. Check small batches (50-100)
4. Use VPN proxies
5. Space out checks

### Bulk Wordlist Processing
1. Create `wordlist.txt` with usernames
2. Use Wordlist tab → Load
3. Select all accounts
4. Start checking
5. Hits auto-save to `hits.txt`

## Performance Tips

- **2-5 accounts** with 1-2s delay = optimal balance
- **5 accounts** with 0.5s delay = maximum speed (risky)
- **Proxies enabled** = safer but slower
- **VPN proxies** = safest but slowest
- **Rotate accounts** = distribute detection risk

## Security Reminders

⚠️ **Use only throwaway test accounts**
- Instagram bans mass checking accounts
- Never use main accounts
- Consider the legal/ToS implications

⚠️ **Credentials stored locally**
- `accounts_state.json` not encrypted
- Keep file secure
- Limit access permissions

⚠️ **Terms of Service**
- May violate Instagram ToS
- Use responsibly
- Respect rate limits

## Where to Go From Here

- **Full Docs**: Read `README.md`
- **Advanced Config**: Check `CONFIGURATION.md`
- **API Details**: See `README.md` → API Endpoints section
- **Troubleshooting**: See `README.md` → Troubleshooting section

## Support

- Check README.md for full documentation
- Review CONFIGURATION.md for advanced setup
- Check browser console (F12) for frontend errors
- Check terminal output for backend errors

## Tech Stack

- **Backend**: Flask 2.3 + Python 3.8+
- **API**: RESTful with CORS
- **Frontend**: Vanilla JavaScript + CSS3
- **Instagram**: instagrapi library
- **Proxies**: HTTP/HTTPS/SOCKS5

## License

For educational purposes. Use responsibly.

---

**Made with ❤️ for username enthusiasts**

**Questions?** Check README.md or CONFIGURATION.md

**Ready?** Run: `python app.py` 🚀
