from django.apps import AppConfig
from pathlib import Path

_path = Path(__file__)

class ApiConfig(AppConfig):
    name = "shared"
    path = _path.parent
