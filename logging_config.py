import logging
from config import LOGS_DIR

LOGS_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format = "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers = [
        logging.StreamHandler(),
        logging.FileHandler(LOGS_DIR / "data.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)