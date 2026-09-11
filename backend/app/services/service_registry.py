import json
import os
from typing import List
from app.schemas.service_schema import CivicService

class ServiceRegistry:
    def __init__(self, data_path: str = None):
        if data_path is None:
            # Default to the demo data file relative to this script
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            data_path = os.path.join(base_dir, "data", "demo", "services.json")
        
        self.data_path = data_path
        self.services: List[CivicService] = self._load_services()

    def _load_services(self) -> List[CivicService]:
        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [CivicService(**item) for item in data]
        except Exception as e:
            print(f"Error loading services: {e}")
            return []

    def get_all_services(self) -> List[dict]:
        return [service.model_dump() for service in self.services]