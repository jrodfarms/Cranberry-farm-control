import json, pathlib
from flask import Flask

def load_json(path, fallback):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return fallback

def create_app():
    app = Flask(__name__)
    root = pathlib.Path(__file__).resolve().parents[1]
    settings = load_json(root / "config" / "settings.json", load_json(root / "config" / "settings.example.json", {}))
    secrets = load_json(root / "config" / "secrets.json", {})
    app.config["APP_SETTINGS"] = settings
    app.config["APP_SECRETS"] = secrets

    from .views import ui
    app.register_blueprint(ui)
    return app
