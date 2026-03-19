#!/usr/bin/env python3
"""
Instagram Username Checker - Termux Edition
Works on Android without instagrapi issues
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import requests
import random
import string
import time
from pathlib import Path
from datetime import datetime
import threading

app = Flask(__name__)
CORS(app)

# ==================== MANAGERS ====================

class Settings:
    def __init__(self):
        self.file = "settings.json"
        self.defaults = {
            "check_delay": 1.0,
            "use_proxies": False,
            "max_accounts": 5,
            "log_hits": True
        }
        self.data = self.load()
    
    def load(self):
        if Path(self.file).exists():
            with open(self.file) as f:
                return json.load(f)
        return self.defaults.copy()
    
    def save(self):
        with open(self.file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def get(self, key, default=None):
        return self.data.get(key, default or self.defaults.get(key))
    
    def set(self, key, value):
        self.data[key] = value
        self.save()


class Accounts:
    def __init__(self):
        self.file = "accounts.json"
        self.data = self.load()
    
    def load(self):
        if Path(self.file).exists():
            with open(self.file) as f:
                return json.load(f)
        return {}
    
    def save(self):
        with open(self.file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def add(self, username, password):
        acc_id = f"{username}_{int(time.time())}"
        self.data[acc_id] = {
            "id": acc_id,
            "username": username,
            "password": password,
            "status": "offline",
            "checks": 0,
            "added": datetime.now().isoformat()
        }
        self.save()
        return acc_id
    
    def get_all(self):
        return self.data
    
    def remove(self, acc_id):
        if acc_id in self.data:
            del self.data[acc_id]
            self.save()
    
    def update(self, acc_id, **kwargs):
        if acc_id in self.data:
            self.data[acc_id].update(kwargs)
            self.save()


class Hits:
    def __init__(self):
        self.file = "hits.txt"
        self.load()
    
    def load(self):
        if not Path(self.file).exists():
            with open(self.file, 'w') as f:
                pass
    
    def add(self, username, timestamp=None, metadata=None):
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        hit = {
            "username": username,
            "timestamp": timestamp,
            "metadata": metadata or {}
        }
        
        with open(self.file, 'a') as f:
            f.write(json.dumps(hit) + '\n')
    
    def get_all(self):
        hits = []
        if Path(self.file).exists():
            with open(self.file) as f:
                for line in f:
                    if line.strip():
                        try:
                            hits.append(json.loads(line))
                        except:
                            pass
        return sorted(hits, key=lambda x: x['timestamp'], reverse=True)
    
    def remove(self, username):
        hits = self.get_all()
        hits = [h for h in hits if h['username'] != username]
        with open(self.file, 'w') as f:
            for hit in hits:
                f.write(json.dumps(hit) + '\n')
    
    def export(self):
        hits = self.get_all()
        return '\n'.join([h['username'] for h in hits])


class Generator:
    CHARS = string.ascii_letters + string.digits + '._'
    
    @staticmethod
    def random(count=10, length=5):
        return [''.join(random.choices(Generator.CHARS, k=random.randint(3, length))) 
                for _ in range(count)]
    
    @staticmethod
    def pattern(base, count=10):
        result = []
        for _ in range(count):
            sep = random.choice(['_', '.', ''])
            suffix = ''.join(random.choices(string.digits, k=random.randint(1, 3)))
            result.append(f"{base}{sep}{suffix}")
        return result
    
    @staticmethod
    def from_file(filepath):
        if Path(filepath).exists():
            with open(filepath) as f:
                return [line.strip() for line in f if line.strip()]
        return []


class Checker:
    def __init__(self):
        self.active = False
        self.progress = {"total": 0, "current": 0, "available": [], "taken": [], "errors": []}
    
    def check_username(self, username, account=None):
        """Check if username is available via Instagram API"""
        try:
            # Try to fetch user info
            headers = {
                'User-Agent': 'Instagram 300.0.0.0.71 Android (31/11; 1080x1920; en_US)'
            }
            
            url = f"https://www.instagram.com/api/v1/users/search/?q={username}"
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('users') and len(data['users']) > 0:
                    return False, "Taken"  # Username exists
                else:
                    return True, "Available"  # Username doesn't exist
            else:
                return None, f"Error: {response.status_code}"
        
        except Exception as e:
            return None, f"Error: {str(e)}"
    
    def start(self, usernames, account_ids):
        self.active = True
        self.progress = {
            "total": len(usernames),
            "current": 0,
            "available": [],
            "taken": [],
            "errors": []
        }
        
        def worker():
            for idx, username in enumerate(usernames):
                if not self.active:
                    break
                
                available, msg = self.check_username(username)
                
                if available is True:
                    self.progress["available"].append(username)
                    if settings.get("log_hits"):
                        hits.add(username)
                elif available is False:
                    self.progress["taken"].append(username)
                else:
                    self.progress["errors"].append((username, msg))
                
                self.progress["current"] = idx + 1
                time.sleep(settings.get("check_delay", 1.0))
            
            self.active = False
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()


# ==================== INITIALIZE ====================

settings = Settings()
accounts = Accounts()
hits = Hits()
checker = Checker()

# ==================== ROUTES ====================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    return jsonify(accounts.get_all())


@app.route('/api/accounts', methods=['POST'])
def add_account():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if username and password:
        acc_id = accounts.add(username, password)
        return jsonify({"success": True, "account_id": acc_id})
    
    return jsonify({"error": "Missing credentials"}), 400


@app.route('/api/accounts/<acc_id>', methods=['DELETE'])
def del_account(acc_id):
    accounts.remove(acc_id)
    return jsonify({"success": True})


@app.route('/api/accounts/<acc_id>/login', methods=['POST'])
def login_account(acc_id):
    acc = accounts.data.get(acc_id)
    if acc:
        accounts.update(acc_id, status="online")
        return jsonify({"success": True, "message": "Logged in"})
    return jsonify({"error": "Account not found"}), 404


@app.route('/api/checker/check', methods=['POST'])
def start_check():
    data = request.json
    usernames = data.get('usernames', [])
    account_ids = data.get('account_ids', [])
    
    if usernames and account_ids:
        checker.start(usernames, account_ids)
        return jsonify({"success": True})
    
    return jsonify({"error": "Missing usernames or accounts"}), 400


@app.route('/api/checker/status', methods=['GET'])
def check_status():
    return jsonify({
        "active": checker.active,
        "progress": int((checker.progress["current"] / checker.progress["total"] * 100) if checker.progress["total"] > 0 else 0),
        "current": checker.progress["current"],
        "total": checker.progress["total"],
        "available": len(checker.progress["available"]),
        "taken": len(checker.progress["taken"]),
        "errors": len(checker.progress["errors"])
    })


@app.route('/api/checker/stop', methods=['POST'])
def stop_check():
    checker.active = False
    return jsonify({"success": True})


@app.route('/api/hits', methods=['GET'])
def get_hits():
    return jsonify(hits.get_all())


@app.route('/api/hits/<username>', methods=['DELETE'])
def del_hit(username):
    hits.remove(username)
    return jsonify({"success": True})


@app.route('/api/hits/export', methods=['GET'])
def export_hits():
    content = hits.export()
    with open('hits_export.txt', 'w') as f:
        f.write(content)
    from flask import send_file
    return send_file('hits_export.txt', as_attachment=True, download_name=f'hits_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')


@app.route('/api/generator/random', methods=['POST'])
def gen_random():
    data = request.json
    count = data.get('count', 10)
    length = data.get('max_length', 5)
    usernames = Generator.random(count, length)
    return jsonify({"usernames": usernames})


@app.route('/api/generator/pattern', methods=['POST'])
def gen_pattern():
    data = request.json
    base = data.get('base', '')
    count = data.get('count', 10)
    usernames = Generator.pattern(base, count)
    return jsonify({"usernames": usernames})


@app.route('/api/generator/wordlist', methods=['POST'])
def gen_wordlist():
    data = request.json
    filepath = data.get('filepath', 'wordlist.txt')
    usernames = Generator.from_file(filepath)
    return jsonify({"usernames": usernames})


@app.route('/api/settings', methods=['GET'])
def get_settings():
    return jsonify(settings.data)


@app.route('/api/settings', methods=['POST'])
def set_settings():
    data = request.json
    for key, value in data.items():
        settings.set(key, value)
    return jsonify({"success": True, "settings": settings.data})


if __name__ == '__main__':
    print("\n" + "="*50)
    print("📸 Instagram Username Checker - Termux Edition")
    print("="*50)
    print("\n✅ All dependencies loaded!")
    print("🌐 Starting server on http://0.0.0.0:5000")
    print("\n📱 Open in browser:")
    print("   http://localhost:5000")
    print("\n⚠️  Make sure templates/index.html exists")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
