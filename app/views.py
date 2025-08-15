import time, threading
from flask import Blueprint, current_app, render_template, request, redirect, url_for, jsonify
from .sensors.mock import MockSensors
from .control.pumps import PumpController

ui = Blueprint("ui", __name__)

_sensors = MockSensors()
_pumps = PumpController()
_bg_thread = None

def _bg_tick():
    while True:
        interval = current_app.config["APP_SETTINGS"].get("update_interval_seconds", 5)
        _sensors.tick()
        # Simple auto logic with PSI + temp thresholds
        if current_app.config["APP_SETTINGS"].get("auto_control_enabled"):
            soil = _sensors.state["soil_moisture"]
            water_ok = _sensors.state["irrigation_water_level_ok"]
            temp_c = _sensors.state["air_temp_c_A"]
            mode = current_app.config["APP_SETTINGS"].get("temp_mode","cool")
            on_th = current_app.config["APP_SETTINGS"].get("temp_on_threshold_c",25)
            off_th = current_app.config["APP_SETTINGS"].get("temp_off_threshold_c",20)
            want_on = False
            if soil == "Dry" and water_ok:
                want_on = True
            if mode == "cool" and temp_c >= on_th:
                want_on = True
            if mode == "cool" and temp_c < off_th:
                want_on = False
            if mode == "heat" and temp_c <= on_th:
                want_on = True
            if mode == "heat" and temp_c > off_th:
                want_on = False
            if _sensors.state["psi"] < current_app.config["APP_SETTINGS"].get("psi_low_cutoff", 15.0):
                want_on = False
            _pumps.set_irrigation(want_on)
        time.sleep(interval)

@ui.before_app_first_request
def start_bg():
    global _bg_thread
    if _bg_thread is None:
        _bg_thread = threading.Thread(target=_bg_tick, daemon=True)
        _bg_thread.start()

@ui.route("/")
def dashboard():
    return render_template("dashboard.html", s=_sensors.state, p=_pumps.state, cfg=current_app.config["APP_SETTINGS"])

@ui.route("/api/state")
def api_state():
    return jsonify({"s": _sensors.state, "p": _pumps.state})

@ui.route("/toggle/irrigation", methods=["POST"])
def toggle_irrigation():
    on = request.form.get("on") == "1"
    _pumps.set_irrigation(on)
    return redirect(url_for("ui.dashboard"))

@ui.route("/settings", methods=["POST"])
def update_settings():
    cfg = current_app.config["APP_SETTINGS"]
    cfg["auto_control_enabled"] = bool(request.form.get("auto_control_enabled"))
    cfg["temp_mode"] = request.form.get("temp_mode","cool")
    cfg["temp_on_threshold_c"] = float(request.form.get("temp_on_threshold_c", cfg.get("temp_on_threshold_c",25)))
    cfg["temp_off_threshold_c"] = float(request.form.get("temp_off_threshold_c", cfg.get("temp_off_threshold_c",20)))
    cfg["psi_low_cutoff"] = float(request.form.get("psi_low_cutoff", cfg.get("psi_low_cutoff",15)))
    return redirect(url_for("ui.dashboard"))
