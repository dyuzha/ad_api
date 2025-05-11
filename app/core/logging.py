import logging
from pathlib import Path
from datetime import datetime

def setup_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s - [UserManager] - %(asctime)s - %(name)s \
        - %(message)s",
        handlers=[
            logging.FileHandler(f"logs/app_{datetime.now().
                                            strftime('%Y%m%d')}.log"),
            logging.StreamHandler()
        ]
    )
