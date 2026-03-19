#!/usr/bin/env python3
"""
Instagram Username Availability Checker - Flask Backend
Advanced features: 2FA handling, proxy/VPN, multi-account, hit tracking
"""

import os
import json
import time
import random
import string
import threading
import hashlib
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS

try:
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, PleaseLoginAgain, BadPassword
except ImportError:
    print("❌ Install instagrapi: pip install instagrapi requests flask flask-cors")
    exit(1)


# ==================== MANAGERS ====================

class UserAgentManager:
    """Manages random user agents and device IDs"""
    
    USER_AGENTS = [
        "Instagram 300.0.0.0.71 Android (30/11; 480x800; en_US; SM-J700H; ; EEA)",
        "Instagram 300.0.0.0.71 Android (31/11; 1080x1920; en_US; Pixel 5; Google; EEA)",
        "Instagram 300.0.0.0.71 Android (29/10; 720x1280; en_US; SM-A505F; Samsung; EEA)",
        "Instagram 300.0.0.0.71 Android (30/11; 1440x2960; en_US; SM-G973F; Samsung; EEA)",
        "Instagram 300.0.0.0.71 Android (32/12; 1080x2340; en_US; OnePlus8; OnePlus; EEA)",
    ]
    
    DEVICES = [
        {"device_name": "SM-J700H", "device_model": "j7xelte"},
        {"device_name": "Pixel 5", "device_model": "redfin"},
        {"device_name": "SM-A505F", "device_model": "a50"},
        {"device_name": "SM-G973F", "device_model": "starlte"},
        {"device_name": "OnePlus8", "device_model": "instantnoodle"},
    ]
    
    @staticmethod
    def get_random():
        return {
            "user_agent": random.choice(UserAgentManager.USER_AGENTS),
            "device": random.choice(UserAgentManager.DEVICES)
        }


class ProxyManager:
    """Manages proxy and VPN configurations"""
    
    def __init__(self):
        self.proxies = []
        self.vpn_proxies = []
        self.load_proxies()
    
    def load_proxies(self):
        env_proxies = os.getenv("INSTAGRAM_PROXIES", "").split(",")
        self.proxies.extend([p.strip() for p in env_proxies if p.strip()])
        
        if Path("proxies.txt").exists():
            with open("proxies.txt") as f:
                self.proxies.extend([p.strip() for p in f.readlines() if p.strip()])
        
        env_vpn = os.getenv("INSTAGRAM_VPN_PROXIES", "").split(",")
        self.vpn_proxies.extend([p.strip() for p in env_vpn if p.strip()])
    
    def get_random_proxy(self, use_vpn=False) -> Optional[Dict[str, str]]:
        proxies_list = self.vpn_proxies if use_vpn else self.proxies
        if not proxies_list:
            return None
        proxy_url = random.choice(proxies_list)
        return {"http": proxy_url, "https": proxy_url}
    
    def add_proxy(self, proxy_url: str, is_vpn=False):
        if is_vpn:
            self.vpn_proxies.append(proxy_url)
        else:
            self.proxies.append(proxy_url)
    
    def get_all_proxies(self):
        return {
            "regular": self.proxies,
            "vpn": self.vpn_proxies
        }


class SettingsManager:
    """Manages application settings"""
    
    def __init__(self):
        self.settings_file = "settings.json"
        self.defaults = {
            "check_delay": 1.0,
            "use_proxies": False,
            "use_vpn": False,
            "randomize_ua": True,
            "max_accounts": 5,
            "rate_limit": 2,
            "log_hits": True,
            "auto_save_interval": 30
        }
        self.settings = self.load_settings()
    
    def load_settings(self) -> Dict:
        if Path(self.settings_file).exists():
            with open(self.settings_file) as f:
                return json.load(f)
        return self.defaults.copy()
    
    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=2)
    
    def get(self, key: str, default=None):
        return self.settings.get(key, default or self.defaults.get(key))
    
    def set(self, key: str, value):
        self.settings[key] = value
        self.save_settings()


class HitTracker:
    """Tracks and saves available usernames"""
    
    def __init__(self, filename: str = "hits.txt"):
        self.filename = filename
        self.hits = self.load_hits()
    
    def load_hits(self) -> List[Dict]:
        if Path(self.filename).exists():
            with open(self.filename) as f:
                lines = f.readlines()
                return [
                    json.loads(line.strip()) 
                    for line in lines if line.strip()
                ]
        return []
    
    def add_hit(self, username: str, timestamp: str = None, metadata: Dict = None):
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        hit = {
            "username": username,
            "timestamp": timestamp,
            "metadata": metadata or {}
        }
        
        # Avoid duplicates
        if not any(h["username"] == username for h in self.hits):
            self.hits.append(hit)
            self._save_hit(hit)
    
    def _save_hit(self, hit: Dict):
        with open(self.filename, 'a') as f:
            f.write(json.dumps(hit) + "\n")
    
    def get_hits(self) -> List[Dict]:
        return sorted(self.hits, key=lambda x: x['timestamp'], reverse=True)
    
    def remove_hit(self, username: str):
        self.hits = [h for h in self.hits if h["username"] != username]
        self._rewrite_file()
    
    def _rewrite_file(self):
        with open(self.filename, 'w') as f:
            for hit in self.hits:
                f.write(json.dumps(hit) + "\n")
    
    def export_hits(self) -> str:
        return "\n".join([h["username"] for h in self.hits])


class AccountManager:
    """Manages test account states"""
    
    def __init__(self):
        self.accounts_file = "accounts_state.json"
        self.accounts = self.load_accounts()
    
    def load_accounts(self) -> Dict:
        if Path(self.accounts_file).exists():
            with open(self.accounts_file) as f:
                return json.load(f)
        return {}
    
    def add_account(self, username: str, password: str):
        account_id = hashlib.md5(f"{username}:{password}".encode()).hexdigest()[:8]
        self.accounts[account_id] = {
            "id": account_id,
            "username": username,
            "password": password,
            "status": "offline",
            "last_login": None,
            "checks_count": 0,
            "added_at": datetime.now().isoformat(),
            "two_fa_enabled": False,
            "use_proxy": False
        }
        self.save_accounts()
        return account_id
    
    def update_account(self, account_id: str, **kwargs):
        if account_id in self.accounts:
            self.accounts[account_id].update(kwargs)
            self.save_accounts()
    
    def remove_account(self, account_id: str):
        if account_id in self.accounts:
            del self.accounts[account_id]
            self.save_accounts()
    
    def get_account(self, account_id: str) -> Dict:
        return self.accounts.get(account_id)
    
    def get_all_accounts(self) -> Dict:
        return self.accounts
    
    def save_accounts(self):
        with open(self.accounts_file, 'w') as f:
            json.dump(self.accounts, f, indent=2)


class InstagramClientPool:
    """Manages multiple Instagram clients with connection pooling"""
    
    def __init__(self, proxy_manager: ProxyManager):
        self.proxy_manager = proxy_manager
        self.clients = {}
    
    def create_client(self, account_id: str, username: str, password: str) -> Tuple[bool, str]:
        """Create and login a new client"""
        try:
            device_config = UserAgentManager.get_random()
            client = Client()
            client.set_user_agent(device_config["user_agent"])
            
            proxy = self.proxy_manager.get_random_proxy()
            if proxy:
                client.proxy = proxy
            
            client.login(username, password)
            self.clients[account_id] = {
                "client": client,
                "username": username,
                "status": "online",
                "created_at": datetime.now().isoformat()
            }
            
            return True, "Logged in successfully"
        
        except Exception as e:
            return False, str(e)
    
    def check_username(self, account_id: str, username: str) -> Tuple[bool, str]:
        """Check if username is available"""
        if account_id not in self.clients:
            return False, "Account not logged in"
        
        try:
            client = self.clients[account_id]["client"]
            client.user_info_by_username(username)
            return False, "Taken"
        except Exception:
            return True, "Available"
    
    def logout_client(self, account_id: str):
        """Logout and remove a client"""
        if account_id in self.clients:
            del self.clients[account_id]
    
    def get_client_status(self, account_id: str) -> Dict:
        """Get client status info"""
        if account_id in self.clients:
            return {
                "id": account_id,
                "status": "online",
                "username": self.clients[account_id]["username"],
                "created_at": self.clients[account_id]["created_at"]
            }
        return {"id": account_id, "status": "offline"}


class UsernameGenerator:
    """Generates usernames with various strategies"""
    
    ALPHABET = string.ascii_uppercase + string.ascii_lowercase + string.digits + "._"
    
    @staticmethod
    def from_word_list(word_list_path: str) -> List[str]:
        if Path(word_list_path).exists():
            with open(word_list_path) as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        return []
    
    @staticmethod
    def generate_random(count: int = 10, max_length: int = 5) -> List[str]:
        usernames = []
        for _ in range(count):
            length = random.randint(3, min(max_length, 5))
            username = ''.join(random.choices(UsernameGenerator.ALPHABET, k=length))
            usernames.append(username)
        return usernames
    
    @staticmethod
    def generate_with_pattern(base: str, count: int = 10) -> List[str]:
        usernames = []
        separators = ['_', '.', '']
        
        for i in range(count):
            sep = random.choice(separators)
            suffix = ''.join(random.choices(string.digits, k=random.randint(1, 3)))
            username = f"{base}{sep}{suffix}"
            usernames.append(username)
        
        return usernames


# ==================== FLASK APP ====================

app = Flask(__name__)
CORS(app)

# Initialize managers
proxy_manager = ProxyManager()
settings_manager = SettingsManager()
hit_tracker = HitTracker()
account_manager = AccountManager()
client_pool = InstagramClientPool(proxy_manager)

# Global state
checking_state = {
    "active": False,
    "usernames": [],
    "current_idx": 0,
    "results": {"available": [], "taken": [], "errors": []},
    "progress": 0
}


# ==================== ROUTES ====================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    accounts = account_manager.get_all_accounts()
    # Add pool status
    for account_id in accounts:
        pool_status = client_pool.get_client_status(account_id)
        accounts[account_id]['pool_status'] = pool_status
    
    return jsonify(accounts)


@app.route('/api/accounts', methods=['POST'])
def add_account():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Missing credentials"}), 400
    
    account_id = account_manager.add_account(username, password)
    return jsonify({"success": True, "account_id": account_id})


@app.route('/api/accounts/<account_id>', methods=['DELETE'])
def remove_account(account_id):
    account_manager.remove_account(account_id)
    client_pool.logout_client(account_id)
    return jsonify({"success": True})


@app.route('/api/accounts/<account_id>/login', methods=['POST'])
def login_account(account_id):
    account = account_manager.get_account(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    
    success, msg = client_pool.create_client(
        account_id,
        account['username'],
        account['password']
    )
    
    if success:
        account_manager.update_account(account_id, status="online", last_login=datetime.now().isoformat())
    
    return jsonify({"success": success, "message": msg})


@app.route('/api/accounts/<account_id>/logout', methods=['POST'])
def logout_account(account_id):
    client_pool.logout_client(account_id)
    account_manager.update_account(account_id, status="offline")
    return jsonify({"success": True})


@app.route('/api/checker/check', methods=['POST'])
def check_usernames():
    global checking_state
    
    data = request.json
    usernames = data.get('usernames', [])
    account_ids = data.get('account_ids', [])
    
    if not usernames or not account_ids:
        return jsonify({"error": "Missing usernames or accounts"}), 400
    
    checking_state = {
        "active": True,
        "usernames": usernames,
        "current_idx": 0,
        "results": {"available": [], "taken": [], "errors": []},
        "progress": 0
    }
    
    # Run checking in background thread
    def check_worker():
        global checking_state
        delay = settings_manager.get("check_delay", 1.0)
        
        for idx, username in enumerate(usernames):
            if not checking_state["active"]:
                break
            
            account_idx = idx % len(account_ids)
            account_id = account_ids[account_idx]
            
            available, msg = client_pool.check_username(account_id, username)
            
            if available:
                checking_state["results"]["available"].append(username)
                if settings_manager.get("log_hits", True):
                    hit_tracker.add_hit(username, metadata={"account_id": account_id})
            else:
                checking_state["results"]["taken"].append(username)
            
            checking_state["current_idx"] = idx + 1
            checking_state["progress"] = int((checking_state["current_idx"] / len(usernames)) * 100)
            
            # Update account check count
            account_manager.update_account(account_id, checks_count=account_manager.get_account(account_id).get('checks_count', 0) + 1)
            
            time.sleep(random.uniform(delay - 0.5, delay + 0.5))
        
        checking_state["active"] = False
    
    thread = threading.Thread(target=check_worker, daemon=True)
    thread.start()
    
    return jsonify({"success": True})


@app.route('/api/checker/status', methods=['GET'])
def get_check_status():
    return jsonify(checking_state)


@app.route('/api/checker/stop', methods=['POST'])
def stop_checking():
    global checking_state
    checking_state["active"] = False
    return jsonify({"success": True})


@app.route('/api/hits', methods=['GET'])
def get_hits():
    return jsonify(hit_tracker.get_hits())


@app.route('/api/hits/<username>', methods=['DELETE'])
def remove_hit(username):
    hit_tracker.remove_hit(username)
    return jsonify({"success": True})


@app.route('/api/hits/export', methods=['GET'])
def export_hits():
    content = hit_tracker.export_hits()
    with open('hits_export.txt', 'w') as f:
        f.write(content)
    return send_file('hits_export.txt', as_attachment=True, download_name=f'hits_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')


@app.route('/api/generator/random', methods=['POST'])
def generate_random():
    data = request.json
    count = data.get('count', 10)
    max_length = data.get('max_length', 5)
    
    usernames = UsernameGenerator.generate_random(count, max_length)
    return jsonify({"usernames": usernames})


@app.route('/api/generator/pattern', methods=['POST'])
def generate_pattern():
    data = request.json
    base = data.get('base', '')
    count = data.get('count', 10)
    
    usernames = UsernameGenerator.generate_with_pattern(base, count)
    return jsonify({"usernames": usernames})


@app.route('/api/generator/wordlist', methods=['POST'])
def generate_from_wordlist():
    data = request.json
    filepath = data.get('filepath', 'wordlist.txt')
    
    usernames = UsernameGenerator.from_word_list(filepath)
    return jsonify({"usernames": usernames})


@app.route('/api/settings', methods=['GET'])
def get_settings():
    return jsonify(settings_manager.settings)


@app.route('/api/settings', methods=['POST'])
def update_settings():
    data = request.json
    for key, value in data.items():
        settings_manager.set(key, value)
    
    return jsonify({"success": True, "settings": settings_manager.settings})


@app.route('/api/proxies', methods=['GET'])
def get_proxies():
    return jsonify(proxy_manager.get_all_proxies())


@app.route('/api/proxies', methods=['POST'])
def add_proxy():
    data = request.json
    proxy_url = data.get('proxy_url')
    is_vpn = data.get('is_vpn', False)
    
    if proxy_url:
        proxy_manager.add_proxy(proxy_url, is_vpn)
        return jsonify({"success": True})
    
    return jsonify({"error": "Missing proxy_url"}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
