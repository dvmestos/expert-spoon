# 📸 Instagram Username Availability Checker - Flask Edition

A sophisticated, production-grade web application for checking Instagram username availability with advanced features including multi-account support, 2FA handling, proxy/VPN support, and real-time hit tracking.

## 🚀 Features

### Core Features
- ✅ **Multi-Account Support** - Up to 5 Instagram test accounts simultaneously
- ✅ **Real-time Checking** - Check unlimited usernames with rotating accounts
- ✅ **2FA Handling** - Automatic detection and SMS/TOTP support
- ✅ **Smart Hit Tracking** - Save available usernames to `hits.txt`
- ✅ **Account Management Panel** - View, login, and remove accounts on the fly
- ✅ **Account Status Monitoring** - See login status, check count, and performance

### Username Generation
- 🎲 **Random Generator** - Generate random usernames with A-Z, a-z, 0-9, `.`, `_`
- 📝 **Pattern Generator** - Create variations (e.g., `cool_123`, `cool.456`)
- 📖 **Wordlist Loader** - Load usernames from text files

### Advanced Features
- 🌐 **Proxy Support** - Configure HTTP/HTTPS proxies and VPN
- 🎭 **User-Agent Randomization** - Rotate realistic Instagram mobile user agents
- 📊 **Real-time Progress** - Live progress bar and statistics during checks
- ⚙️ **Settings Panel** - Customize delay, rate limiting, and features
- 💾 **Hit Export** - Download all found usernames as `.txt`

### UI/UX
- 🎨 **Dark Neon Aesthetic** - Cyberpunk-inspired interface with cyan/pink accents
- 📱 **Responsive Design** - Works on desktop and mobile browsers
- ⚡ **Smooth Animations** - CSS-based transitions and micro-interactions
- 🎯 **Intuitive Layout** - Three-panel design for accounts, checker, and hits

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)
- Modern web browser

## 🔧 Installation

### 1. Clone or download the project
```bash
cd instagram-checker
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Directory Structure
```
instagram-checker/
├── app.py                          # Flask backend
├── requirements.txt                # Python dependencies
├── templates/
│   └── index.html                 # Frontend UI
├── settings.json                  # App settings (auto-created)
├── accounts_state.json            # Account states (auto-created)
├── hits.txt                       # Available usernames (auto-created)
└── proxies.txt                    # (Optional) Proxy list
```

The HTML file should be placed in a `templates/` folder:
```bash
mkdir -p templates
# Copy index.html to templates/index.html
```

## 🚀 Running the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Docker Option (Alternative)
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

## 📖 Usage Guide

### 1. Adding Accounts

1. Click **"+ Add"** in the Accounts panel
2. Enter Instagram username and password
3. Account will be saved locally
4. Click **"Login"** to authenticate (2FA supported)
5. Account status changes to **"Online"**

> **Security Note**: Credentials are stored locally in `accounts_state.json`. Use throwaway test accounts only.

### 2. Username Generation

#### Manual Entry
- Switch to **"Manual"** tab
- Paste or type usernames (one per line)
- Click anywhere to load the list

#### Random Generator
1. Go to **"Random"** tab
2. Set count (1-100) and max length (1-10)
3. Click **"Generate Random"**
4. Usernames use A-Z, a-z, 0-9, `.`, `_`

#### Pattern Generator
1. Go to **"Pattern"** tab
2. Enter base name (e.g., "cool")
3. Set count
4. Click **"Generate Pattern"**
5. Creates variations like `cool_123`, `cool.456`

#### Wordlist Loader
1. Create a text file with usernames (one per line)
2. Go to **"Wordlist"** tab
3. Enter file path (e.g., `wordlist.txt`)
4. Click **"Load Wordlist"**

### 3. Checking Usernames

1. Select usernames using a generator or manual entry
2. Select accounts in the **"Select Accounts"** section
3. Click **"Login All"** to ensure all accounts are online
4. Click **"Start Checking"**
5. Watch real-time progress bar and statistics
6. Available usernames appear in **"Hits"** panel
7. Results are automatically saved to `hits.txt`

### 4. Managing Hits

- **View**: All available usernames shown in right panel
- **Remove**: Click **"✕"** next to any hit to remove
- **Export**: Click **"Export"** to download all hits as `.txt`

### 5. Settings

Click **⚙️ Settings** to configure:
- **Check Delay**: Wait between checks (seconds)
- **Rate Limit**: Enforce rate limiting
- **Use Proxies**: Enable proxy rotation
- **Use VPN**: Route through VPN
- **Log Hits**: Auto-save available usernames

## 🔐 2FA Handling

When 2FA is detected:
1. Choose method: **SMS** or **TOTP** (authenticator app)
2. Enter the code from SMS or authenticator
3. Login automatically completes
4. Account status shows "Online"

## 🌐 Proxy Configuration

### Option 1: Environment Variables
```bash
export INSTAGRAM_PROXIES="http://proxy1:8080,http://proxy2:8080"
export INSTAGRAM_VPN_PROXIES="http://vpn1:8080,http://vpn2:8080"
python app.py
```

### Option 2: File-based
Create `proxies.txt`:
```
http://proxy1:8080
http://proxy2:8080
socks5://proxy3:1080
```

### Option 3: Web Panel
1. Open Settings
2. Enable "Use Proxies" or "Use VPN"
3. Proxies rotate automatically during checks

## 📊 API Endpoints

### Accounts
- `GET /api/accounts` - List all accounts
- `POST /api/accounts` - Add account
- `DELETE /api/accounts/<id>` - Remove account
- `POST /api/accounts/<id>/login` - Login account
- `POST /api/accounts/<id>/logout` - Logout account

### Checker
- `POST /api/checker/check` - Start checking
- `GET /api/checker/status` - Get progress status
- `POST /api/checker/stop` - Stop checking

### Hits
- `GET /api/hits` - Get all hits
- `DELETE /api/hits/<username>` - Remove hit
- `GET /api/hits/export` - Download hits file

### Generator
- `POST /api/generator/random` - Generate random usernames
- `POST /api/generator/pattern` - Generate pattern variants
- `POST /api/generator/wordlist` - Load from wordlist

### Settings
- `GET /api/settings` - Get current settings
- `POST /api/settings` - Update settings

## 📁 File Outputs

### `hits.txt`
Contains all found available usernames in JSON format:
```json
{"username": "available_user", "timestamp": "2024-01-15T10:30:00", "metadata": {"account_id": "abc123"}}
{"username": "cool.name", "timestamp": "2024-01-15T10:35:00", "metadata": {"account_id": "xyz789"}}
```

Export to clean text with the **"Export"** button.

### `settings.json`
Stores your preferences:
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

### `accounts_state.json`
Stores account credentials and state:
```json
{
  "abc123": {
    "id": "abc123",
    "username": "test_account",
    "password": "encrypted_or_plain",
    "status": "online",
    "checks_count": 150,
    "added_at": "2024-01-15T10:00:00"
  }
}
```

## ⚙️ Advanced Configuration

### Rate Limiting
- Set check delay to 1-3 seconds to avoid detection
- Enable rate limit in settings
- Use multiple accounts to distribute requests

### Proxy Rotation
- Add proxies via environment or file
- Enable in settings
- Proxies rotate per check

### Device/UA Spoofing
- Automatically enabled by default
- Rotates between 5 realistic Android devices
- Each login gets random user agent

## 🚨 Troubleshooting

### "Login failed" Error
- Check username/password
- Try manual login in web UI
- Check if account has 2FA enabled

### "Account not logged in" During Check
- Ensure all accounts are marked "Online"
- Click "Login All" before checking
- Check account status in panel

### Slow Checking Speed
- Reduce check delay in settings
- Add more test accounts
- Disable proxy if not needed

### Hits Not Saving
- Check "Log Hits" is enabled in settings
- Verify write permissions in directory
- Check `hits.txt` file exists

### Connection Issues
- Test proxy settings with curl
- Check internet connection
- Verify API is running on correct port (5000)

## 🔒 Security Notes

⚠️ **Use Only Throwaway Accounts**
- Instagram will likely ban accounts used for mass checking
- Use dedicated test accounts only
- Never use main accounts

⚠️ **Credential Storage**
- Credentials stored in `accounts_state.json`
- Not encrypted by default
- Secure the file and directory
- Consider using environment variables for sensitive data

⚠️ **Terms of Service**
- Bulk username checking may violate Instagram ToS
- Use responsibly and within Instagram's guidelines
- Risk of account suspension/ban

## 📈 Performance Tips

- **Optimal**: 2-5 accounts, 1-2 second delay, no proxies
- **With Proxies**: 3-5 accounts, 2-3 second delay
- **Wordlist Mode**: 5 accounts, longer lists, 1-2 second delay
- **Max Throughput**: Use all 5 accounts, rotate proxies, 0.5-1s delay

## 🐛 Debugging

Enable Flask debug mode:
```python
app.run(debug=True)
```

Check browser console (F12) for frontend errors.

Check terminal output for backend errors.

## 📝 Logs

All activity is logged to browser console and terminal:
- Account login/logout
- Check progress
- Proxy rotation
- Hit detection
- Errors and warnings

## 🤝 Contributing

Improvements welcome! Potential enhancements:
- Database backend for larger scale
- Advanced analytics dashboard
- Instagram API v2 integration
- Captcha bypass
- Advanced anti-detection

## ⚖️ License

This project is for educational purposes only. Use responsibly.

## 📚 References

- [instagrapi Documentation](https://github.com/subzeroid/instagrapi)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Instagram Security](https://help.instagram.com/1948495274694637)

---

**Made with ❤️ for username hunting enthusiasts**
