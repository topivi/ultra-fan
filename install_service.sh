#!/usr/bin/env bash
set -Eeuo pipefail

if [[ ${EUID} -ne 0 ]]; then
  echo "This installer must be run as root (or with sudo)."
  echo "Example: sudo bash $0"
  exit 1
fi

SOURCE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="/opt/ultra-fan"
SERVICE_FILE="/etc/systemd/system/dell-fan.service"

if [[ ! -f "${SOURCE_DIR}/ultra_fan.py" ]]; then
  echo "Error: ultra_fan.py not found in ${SOURCE_DIR}"
  exit 1
fi

mkdir -p /opt
rm -rf "${TARGET_DIR}"
cp -a "${SOURCE_DIR}/." "${TARGET_DIR}/"
chmod +x "${TARGET_DIR}/ultra_fan.py"

cat > "${SERVICE_FILE}" <<'EOF'
[Unit]
Description=Ultra Fan Controller for Dell systems
After=multi-user.target
Wants=multi-user.target
StartLimitIntervalSec=0

[Service]
Type=simple
WorkingDirectory=/opt/ultra-fan
ExecStart=/usr/bin/python3 -u /opt/ultra-fan/ultra_fan.py
Restart=always
RestartSec=5
User=root
Group=root
Environment=PYTHONUNBUFFERED=1
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now dell-fan.service
systemctl status --no-pager dell-fan.service --lines 20 || true

echo
printf 'Installed and started: %s\n' "${TARGET_DIR}"
printf 'Service file: %s\n' "${SERVICE_FILE}"
printf 'Check status with: sudo systemctl status dell-fan.service\n'