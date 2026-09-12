import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def load_json(filename: str, fallback=None):
    """Load JSON data from project/data/ with optional fallback."""
    filepath = DATA_DIR / filename
    try:
        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
    return fallback if fallback is not None else {}
