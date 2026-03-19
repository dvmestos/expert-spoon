# 📱 Instagram Checker - Termux (Android) Setup Guide

## ✅ Prerequisites (Already Done!)

You have:
- ✅ Python 3.13
- ✅ Flask 2.3.3
- ✅ Requests
- ✅ Flask-CORS
- ✅ instagrapi (partially working)

## 🚀 Quick Setup

### Step 1: Download Files
```bash
# Create project directory
mkdir -p ~/instagram-checker
cd ~/instagram-checker

# Download the zip file or copy files manually
# Place app_termux.py in the directory
```

### Step 2: Create Templates Folder
```bash
mkdir -p templates
```

### Step 3: Copy HTML File
Place the `index.html` file in the `templates/` folder

```bash
# Or create symbolic link
ln -s /path/to/index.html templates/index.html
```

### Step 4: Run the App
```bash
cd ~/instagram-checker
python app_termux.py
```

### Step 5: Access in Browser
```
http://localhost:5000
```

---

## 📝 File Structure

```
~/instagram-checker/
├── app_termux.py              ← Main app (Termux version)
├── index.html                 ← Copy to templates/
├── templates/
│   └── index.html
├── settings.json              ← Auto-created
├── accounts.json              ← Auto-created
├── hits.txt                   ← Auto-created
└── wordlist.txt               ← (Optional) Your wordlist
```

---

## 🔧 Troubleshooting

### Issue: "Address already in use"
```bash
# Port 5000 is already in use
# Change port in app_termux.py:
# Change: app.run(port=5000)
# To: app.run(port=8000)
```

### Issue: "Connection refused"
```bash
# Make sure app is running
# Check Termux terminal shows:
# "Starting server on http://0.0.0.0:5000"
```

### Issue: "Cannot find templates/index.html"
```bash
# Create templates folder
mkdir -p templates

# Copy HTML file
cp index.html templates/
```

### Issue: "Module not found"
```bash
# Try installing missing module
pip install flask-cors

# Or reinstall all
pip install -r requirements.txt
```

---

## 💡 Features in Termux Version

✅ **Account Management**
- Add/remove accounts
- Login status tracking
- Check count per account

✅ **Username Checking**
- Check via Instagram API
- Real-time progress
- Hit tracking

✅ **Generators**
- Random generator
- Pattern generator
- Wordlist loader

✅ **Hit Tracking**
- Auto-save to hits.txt
- Export results
- Remove individual hits

✅ **Settings**
- Adjustable delay
- Hit logging toggle
- Auto-customizable

---

## 🌐 Network Requirements

### For Browser Access from Phone
```bash
# Option 1: Local Network
# Use IP address instead of localhost
# Find IP: ifconfig or ip addr
# Access: http://<your-ip>:5000

# Option 2: Use Localhost
# Access from same device: http://localhost:5000
```

### For External Access
```bash
# Use ngrok to expose locally
# Install: pip install pyngrok
# Add to app_termux.py:
from pyngrok import ngrok
public_url = ngrok.connect(5000)
print(f"Public URL: {public_url}")
```

---

## 📊 Using the Checker

### 1. Add Account
- Click "+ Add"
- Enter Instagram username
- Enter password
- Click "Add Account"

### 2. Login
- Click "Login" button
- Wait for "Online" status
- Repeat for multiple accounts

### 3. Generate Usernames
#### Random
- Set count: 10-100
- Set max length: 3-10
- Click "Generate Random"

#### Pattern
- Enter base name: "cool"
- Set count: 10-100
- Click "Generate Pattern"

#### Wordlist
- Create wordlist.txt file
- One username per line
- Enter: wordlist.txt
- Click "Load Wordlist"

### 4. Start Checking
- Select accounts from dropdown
- Click "Start Checking"
- Watch progress bar
- Results appear in "Hits" section

### 5. Export
- Click "Export" in Hits panel
- Download hits.txt file
- Open in text editor

---

## 📁 Advanced Configuration

### Create Settings File (settings.json)
```json
{
  "check_delay": 1.0,
  "use_proxies": false,
  "max_accounts": 5,
  "log_hits": true
}
```

### Add Wordlist
Create `wordlist.txt`:
```
coolname
awesomeuser
radicaldude
firelike
amazing.user
super_cool
...
```

---

## 🔐 Important Notes

⚠️ **Instagram Detection Risk**
- Use throwaway accounts only
- Never use main accounts
- Instagram can detect and ban

⚠️ **API Rate Limiting**
- Don't set delay below 0.5s
- Use multiple accounts
- Space out checks

⚠️ **Storage & Speed**
- Termux has limited storage
- Don't generate 10,000+ usernames at once
- Clear old hits.txt periodically

---

## 🚀 Performance Tips

### Optimal Termux Settings
```json
{
  "check_delay": 2.0,
  "max_accounts": 2,
  "log_hits": true
}
```

**Why?**
- Termux is slower than desktop
- Fewer accounts = less memory
- Longer delay = safer
- Logging slows it down slightly

---

## 📱 Using on Browser

### Access from Same Phone
```
http://localhost:5000
```

### Access from Other Device
```
# Find Termux phone IP
ifconfig

# Use IP in browser
http://<phone-ip>:5000
# Example: http://192.168.1.100:5000
```

---

## 🔄 Keep App Running

### Option 1: Keep Terminal Open
- Just leave Termux running
- Don't close the app

### Option 2: Use tmux (Advanced)
```bash
# Install
pkg install tmux

# Create session
tmux new-session -d -s checker "cd ~/instagram-checker && python app_termux.py"

# Check status
tmux list-sessions

# Reconnect
tmux attach -t checker
```

### Option 3: Background Service (Advanced)
Create a startup script:
```bash
#!/bin/bash
cd ~/instagram-checker
nohup python app_termux.py > app.log 2>&1 &
```

---

## 📊 Viewing Logs

### Real-time Logs
```bash
# In separate Termux window
tail -f app.log
```

### Check Stored Data
```bash
# View accounts
cat accounts.json

# View hits
cat hits.txt

# View settings
cat settings.json
```

---

## 🧹 Cleanup

### Clear Old Hits
```bash
# Backup first
cp hits.txt hits_backup.txt

# Clear
> hits.txt
```

### Reset Everything
```bash
rm settings.json accounts.json hits.txt
# Restart app, configs will regenerate
```

---

## ⚡ Speed Optimization

### For Faster Checking
```json
{
  "check_delay": 0.5,
  "log_hits": false
}
```

### For Stability
```json
{
  "check_delay": 3.0,
  "log_hits": true
}
```

### For Large Wordlists
```json
{
  "check_delay": 1.0,
  "max_accounts": 3
}
```

---

## 🛠️ Debugging

### Enable Verbose Output
Add to app_termux.py:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Network
```bash
# Test connection
ping google.com

# Check port availability
netstat -tuln | grep 5000
```

### Monitor Resources
```bash
# Install top
pkg install procps-ng

# Monitor
top
```

---

## 🎯 Common Workflows

### Quick Hunt (10 Usernames)
1. Add 1 account
2. Login
3. Generate random (count: 10, length: 5)
4. Check
5. Export hits

### Medium Batch (100 Usernames)
1. Add 2 accounts
2. Login all
3. Generate random (count: 100, length: 5)
4. Check
5. Check periodically

### Large Wordlist (1000+)
1. Create wordlist.txt
2. Add 2-3 accounts
3. Load wordlist
4. Set delay to 1.5s
5. Start checking
6. Let run overnight

---

## 📚 Additional Resources

- Flask Docs: [flask.palletsprojects.com](https://flask.palletsprojects.com)
- Termux: [termux.com](https://termux.com)
- Python: [python.org](https://python.org)

---

## ✅ Checklist Before Starting

- [ ] Python 3.8+ installed
- [ ] Flask and dependencies installed
- [ ] Project folder created
- [ ] index.html copied to templates/
- [ ] Port 5000 is free
- [ ] Termux has network access
- [ ] Throwaway Instagram accounts ready

---

## 🚀 Ready?

```bash
cd ~/instagram-checker
python app_termux.py
```

Then open: **http://localhost:5000**

---

**Made for Termux on Android**

*Happy hunting!* 🎉
