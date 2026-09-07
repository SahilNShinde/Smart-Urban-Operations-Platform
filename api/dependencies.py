"""
API dependencies for loading models and database manager.
Member 1: Data Engineering & Machine Learning
"""

import os
import sys
from typing import Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from ml.models.traffic_model import MumbaiTrafficModel
from ml.models.flood_model import MumbaiFloodModel
from database.db_manager import DatabaseManager

SAVED_MODELS_DIR = os.path.join(BASE_DIR, "ml", "saved_models")

_traffic_model: Optional[MumbaiTrafficModel] = None
_flood_model: Optional[MumbaiFloodModel] = None
_db_manager: Optional[DatabaseManager] = None


def get_db_manager() -> DatabaseManager:
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager


def get_traffic_model() -> MumbaiTrafficModel:
    global _traffic_model
    if _traffic_model is None:
        _traffic_model = MumbaiTrafficModel.load(SAVED_MODELS_DIR)
    return _traffic_model


def get_flood_model() -> MumbaiFloodModel:
    global _flood_model
    if _flood_model is None:
        _flood_model = MumbaiFloodModel.load(SAVED_MODELS_DIR)
    return _flood_model
