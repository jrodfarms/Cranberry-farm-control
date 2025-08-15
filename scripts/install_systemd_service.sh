#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")"/.. && pwd)"
SERVICE="/etc/systemd/system/cranberry.service"

sudo bash -c "cat > $SERVICE" <<'UNIT'
[Unit]
Description=Cranberry Farm HMI
After=network-online.target
Wants=network-online.target

[Service]
WorkingDirectory=%h/cranberry-farm-control
Environment=FLASK_ENV=production
ExecStart=%h/cranberry-farm-control/.venv/bin/python run.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
UNIT

echo "Reloading systemd..."
sudo systemctl daemon-reload
echo "Created service cranberry.service"
