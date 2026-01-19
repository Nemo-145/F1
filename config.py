from enum import Enum
from pathlib import Path

# Основные настройки F1
YEAR: int = 2024
GRAND_PRIX: str = "Abu Dhabi"    
SESSION_TYPE: str = "R"          # "R" – Race, "Q" – Qualifying, "P" – Practice

START_YEAR: int = 2022
END_YEAR: int = 2025
SEASONS: list[int] = list(range(START_YEAR, END_YEAR + 1))

class SessionTypes(Enum):
    PRACTICE = "P"
    QUALIFYING = "Q"
    RACE = "R"



# Пути
PROJECT_ROOT: Path = Path(__file__).resolve().parent
DATA_RAW_DIR: Path = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_DIR: Path = PROJECT_ROOT / "data" / "processed"
MODELS_DIR: Path = PROJECT_ROOT / "models"
REPORTS_DIR: Path = PROJECT_ROOT / "reports"
CACHE_DIR: Path = PROJECT_ROOT / "cache"
LOGS_DIR: Path = PROJECT_ROOT / "logs"


# ML / обучение
TEST_SIZE: float = 0.2
RANDOM_STATE: int = 42

# MLflow 
MLFLOW_TRACKING_URI: str = "http://localhost:5000"
MLFLOW_EXPERIMENT_NAME: str = "f1-pet-project"
