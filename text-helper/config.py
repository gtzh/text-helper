import yaml
from pathlib import Path

_CONFIG_PATH = Path(__file__).parent / "config.yaml"
_config = None


def _load():
    global _config
    with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
        _config = yaml.safe_load(f)
    return _config


def get_default_model():
    cfg = _load()
    for m in cfg.get("models", []):
        if m.get("default"):
            return m["id"]
    # fallback
    models = cfg.get("models", [])
    return models[0]["id"] if models else "gpt-4o"


def get_models():
    return _load().get("models", [])


def get_operation(operation_key):
    cfg = _load()
    ops = cfg.get("operations", {})
    return ops.get(operation_key, {})


def get_operations():
    return _load().get("operations", {})


def get_newapi_config():
    return _load().get("newapi", {})


def get_popup_config():
    return _load().get("popup", {})
