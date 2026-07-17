#!/usr/bin/env bash
set -e

DEFAULT_PATH="$HOME/.local/bin/cyassist"

read -p "Install cyassist to [$DEFAULT_PATH]: " INSTALL_PATH
INSTALL_PATH="${INSTALL_PATH:-$DEFAULT_PATH}"

INSTALL_DIR=$(dirname "$INSTALL_PATH")
mkdir -p "$INSTALL_DIR"

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

cat > "$INSTALL_PATH" << 'WRAPPER'
#!/usr/bin/env bash
# Cyassist v3.0 — Engine-driven bug bounty assistant
exec python3 "<<REPO_DIR>>/cyassist.py" "$@"
WRAPPER

sed -i "s|<<REPO_DIR>>|$REPO_DIR|g" "$INSTALL_PATH"
chmod +x "$INSTALL_PATH"

echo "Installed cyassist to $INSTALL_PATH"
echo ""
echo "Make sure $INSTALL_DIR is in your PATH."
echo "Run: cyassist --help"
echo "  or: cyassist --version"
