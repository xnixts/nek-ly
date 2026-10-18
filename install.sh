#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

if [ -z "${PREFIX:-}" ] || [ ! -d "$PREFIX" ]; then
  echo "This installer is intended for Termux on Android."
  echo "Install Termux first, then run this script inside Termux."
  exit 1
fi

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$HOME/.local/share/nek-ly"
BIN_DIR="$PREFIX/bin"

echo "=================================="
echo "          NEK LY 1.0"
echo "  Linux learning environment"
echo "=================================="

pkg update
pkg install -y python proot-distro git

mkdir -p "$APP_DIR" "$BIN_DIR"
cp "$PROJECT_DIR/nekly.py" "$APP_DIR/nekly.py"
cp "$PROJECT_DIR/config.json" "$APP_DIR/config.json"
chmod 755 "$APP_DIR/nekly.py"

cat > "$BIN_DIR/nekly" <<'LAUNCHER'
#!/data/data/com.termux/files/usr/bin/bash
exec python "$HOME/.local/share/nek-ly/nekly.py" "$@"
LAUNCHER
chmod 755 "$BIN_DIR/nekly"

echo
echo "[OK] Nek Ly installed."
echo "Start it with: nekly"
echo "Optional Debian environment: nekly install-linux"
