#!/bin/bash
echo ""
echo "================================================"
echo "  MSI Campus Digital Signage System"
echo "================================================"
echo ""

if ! command -v python3 &>/dev/null; then
    echo "[ERROR] Python 3 not found. Install from https://www.python.org/downloads/"
    exit 1
fi
echo "[OK] Python: $(python3 --version)"

echo "[..] Installing packages..."
pip3 install flask flask-cors werkzeug openpyxl --quiet --disable-pip-version-check
echo "[OK] Packages ready."
echo ""

LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || hostname -I 2>/dev/null | awk '{print $1}' || echo "unknown")
echo "================================================"
echo "  Login / Admin : http://localhost:5000"
echo "  TV Display    : http://$LOCAL_IP:5000/display"
echo "================================================"
echo ""

sleep 2 && open "http://localhost:5000" 2>/dev/null &
python3 server.py
