import logging
from pathlib import Path
from datetime import datetime


class LoggerConfigurator:
    def __init__(self, log_dir: str = "logs", log_level: int = logging.DEBUG):
        self.log_dir = Path(log_dir)
        self.log_level = log_level

    def setup(self) -> None:
        self.log_dir.mkdir(exist_ok=True)

        log_file = self.log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"

        logging.basicConfig(
            level=self.log_level,
            format="%(levelname)s - [AD API] - %(asctime)s - %(name)s - %(message)s",
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
