"""
Logging configuration for Safe DeFi Assistant
"""

import logging
import sys
from pathlib import Path
from infrastructure.config.settings import config

def setup_logging():
    """Setup application logging"""
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_dir / config.LOG_FILE)
        ]
    )
    
    # Set specific loggers
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    
    return logging.getLogger(__name__)

# Initialize logger
logger = setup_logging()
