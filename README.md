# Cranberry Farm Control – Starter (Mock HMI)

This starter gives you a **mobile-friendly Flask HMI** with **Mock Sensor Mode** so you can see the dashboard running on your Raspberry Pi before wiring any hardware.

### Features
- Live dashboard cards (Air & Soil temps, PSI, Flood heights, Drain float)
- Manual Irrigation toggle
- Auto-control placeholders (PSI cutoff + temp thresholds)
- Config files with sensible defaults
- Systemd install script (optional run-on-boot)

### Quick Start (Raspberry Pi OS with Desktop)

```bash
sudo apt update && sudo apt -y install python3-pip python3-venv
git clone <your repo url> cranberry-farm-control
cd cranberry-farm-control
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp config/settings.example.json config/settings.json
cp config/secrets.example.json config/secrets.json
python run.py
```
Open `http://raspberrypi.local:5000` (or `http://<Pi-IP>:5000`).

### Next Steps
- Replace `app/sensors/mock.py` with real drivers later.
- Hook GPIO in `app/control/pumps.py` for your relays.
- Fill in alerts credentials in `config/secrets.json` when ready.
