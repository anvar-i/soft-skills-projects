"""Read and write the simulator's single JSON data file."""

import json
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent / "storage" / "storage.json"


class StorageError(Exception):
    """The saved data cannot be read or written safely."""


class JsonStorage:
    def __init__(self, path=DATA_FILE):
        self.path = Path(path)

    def load(self):
        if not self.path.exists() or self.path.stat().st_size == 0:
            return {}
        try:
            with self.path.open("r", encoding="utf-8") as source:
                data = json.load(source)
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise StorageError(f"Cannot read {self.path}: {error}") from error
        if not isinstance(data, dict):
            raise StorageError("The JSON root must be an object of email keys.")
        return data

    def save(self, data):
        temporary = self.path.with_name(self.path.name + ".tmp")
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with temporary.open("w", encoding="utf-8") as target:
                json.dump(data, target, ensure_ascii=False, indent=2)
                target.write("\n")
            temporary.replace(self.path)
        except (OSError, TypeError, ValueError) as error:
            temporary.unlink(missing_ok=True)
            raise StorageError(f"Cannot save {self.path}: {error}") from error
