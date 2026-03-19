#!/bin/bash
# Quick setup script for Instagram Username Checker

echo "📸 Instagram Username Checker - Setup"
echo "========================================"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Install Python 3.8+"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create directories
echo "📁 Creating directory structure..."
mkdir -p templates

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create initial files
echo "📝 Creating configuration files..."

# Create empty settings if not exists
if [ ! -f settings.json ]; then
    cat > settings.json << 'EOF'
{
  "check_delay": 1.0,
  "use_proxies": false,
  "use_vpn": false,
  "randomize_ua": true,
  "max_accounts": 5,
  "rate_limit": 2,
  "log_hits": true,
  "auto_save_interval": 30
}
EOF
    echo "✅ Created settings.json"
fi

# Create empty accounts state
if [ ! -f accounts_state.json ]; then
    echo "{}" > accounts_state.json
    echo "✅ Created accounts_state.json"
fi

# Create hits file
if [ ! -f hits.txt ]; then
    touch hits.txt
    echo "✅ Created hits.txt"
fi

# Create proxies template
if [ ! -f proxies.txt ]; then
    cat > proxies.txt << 'EOF'
# Add proxies here (one per line)
# http://proxy1:8080
# http://proxy2:8080
# socks5://proxy3:1080
EOF
    echo "✅ Created proxies.txt (template)"
fi

echo ""
echo "✨ Setup complete!"
echo ""
echo "📖 Next steps:"
echo "1. Copy templates/index.html to the templates folder"
echo "2. Run: python app.py"
echo "3. Open browser: http://localhost:5000"
echo ""
echo "🚀 Happy username hunting!"
