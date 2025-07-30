import logging
import os
from datetime import datetime
from typing import Optional

class SyllaboLogger:
    def __init__(self, name: str = "syllabo", log_file: Optional[str] = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # File handler
            if not log_file:
                log_file = f"logs/syllabo_{datetime.now().strftime('%Y%m%d')}.log"
            
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            
            # Formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(formatter)
            file_handler.setFormatter(formatter)
            
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)
    
    def info(self, message: str):
        self.logger.info(message)
    
    def error(self, message: str):
        self.logger.error(message)
    
    def warning(self, message: str):
        self.logger.warning(message)
    
    def debug(self, message: str):
        self.logger.debug(message)