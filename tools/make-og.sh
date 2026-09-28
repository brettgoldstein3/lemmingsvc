#!/bin/sh
# Render tools/og-card.html to og.png (1200x630) with headless Chrome.
# Needs a local server on :8742 serving this repo (python3 -m http.server 8742).
set -e
cd "$(dirname "$0")/.."
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size=1200,630 --virtual-time-budget=4000 \
  --screenshot="$PWD/og.png" http://localhost:8742/tools/og-card.html 2>/dev/null
echo "wrote og.png"
