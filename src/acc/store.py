from pydantic import BaseModel, ConfigDict, Field
from typing import Dict, Any
import json

class Store(BaseModel):
    versions: Dict[int, Dict[str, Any]] = Field(default_factory=dict)
    current_version: int = 0

    def add_version(self, data: Dict[str, Any]):
        self.current_version += 1
        self.versions[self.current_version] = data

    def get_version(self, version: int) -> Dict[str, Any]:
        if version not in self.versions:
            raise ValueError("Version {version} of data not exist before.")
        return self.versions.get(version, {})

    def get_current_version(self) -> Dict[str, Any]:
        return self.get_version(self.current_version)

    def rollback(self, version: int):
        if version in self.versions:
            self.current_version = version
        else:
            raise ValueError(f"Version {version} does not exist")

    def list_versions(self) -> Dict[int, Dict[str, Any]]:
        return self.versions

    def save_to_file(self, filename: str):
        """Save the current state to a JSON file."""
        data = {
            "versions": {int(k): v for k, v in self.versions.items()},
            "current_version": self.current_version
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load_from_file(cls, filename: str) -> 'Store':
        """Load the state from a JSON file and return a new RAStore instance."""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        store = cls()
        store.versions = {int(k): v for k, v in data["versions"].items()}
        store.current_version = int(data["current_version"])
        return store