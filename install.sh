#!/usr/bin/env bash
set -e
UPKVER="1.0-beta3"
echo "-> installing upk"
if ! tar --help 2>&1 | grep -q 'xz'; then
  echo "tar is not installed or does not support xz"
  exit 1
fi

if ! command -v git >/dev/null; then
  echo "git is not installed"
  exit 1
fi

if command -v python3 >/dev/null; then
  PYTHON=$(command -v python3)
else
  PYTHON="INSTALL"
fi

CACHE_DIR="$HOME/.upk/cache"
INSTALL_DIR="$CACHE_DIR/install"
mkdir -p "$INSTALL_DIR"

if [ "$PYTHON" = "INSTALL" ]; then
  mkdir -p "$INSTALL_DIR/python3"
  curl -L -o "$INSTALL_DIR/python3-3.14.0a7.tar.xz" https://upk.juanvel400.xyz/pool/python3-3.14.0a7.upk
  tar -xf "$INSTALL_DIR/python3-3.14.0a7.tar.xz" -C "$INSTALL_DIR/python3"
  PYTHON="$INSTALL_DIR/python3/bin/python3.14"
fi
echo "-> getting upk"
git clone https://github.com/juanvel4000/upk "$CACHE_DIR/firstinstallation"

echo "-> bootstrapping upk"
curl -o "$CACHE_DIR/firstinstallation/upk-$UPKVER.upk" "https://upk.juanvel400.xyz/pool/upk-$UPKVER.upk"
$PYTHON "$CACHE_DIR/firstinstallation/upk.py" install-local "$CACHE_DIR/firstinstallation/upk-$UPKVER.upk"

#echo "-> cleaning up"
#rm -rf "$INSTALL_DIR"
#rm -rf "$CACHE_DIR/firstinstallation"

echo "-> adding upk to your path"
SHELL_NAME=$(basename "$SHELL")
RC_FILE="$HOME/.${SHELL_NAME}rc"
if ! grep -q "$HOME/.upk/bin" "$RC_FILE"; then
  echo "export PATH=\$PATH:$HOME/.upk/bin" >> "$RC_FILE"
fi
echo "-> doing a final check"
if command -v upk >/dev/null 2>&1; then
  echo "upk has been installed"
  exit 0
else
  echo "error installing upk"
  exit 1
fi
