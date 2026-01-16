"""Logging utility for consistent logging configuration."""

import logging
import sys
from pathlib import Path
from typing import Optional
from utils.core.config import LOG_LEVEL, LOGS_DIR


def setup_logging(
    level: Optional[str] = None,
    format_string: Optional[str] = None,
    log_to_file: bool = False,
    log_file: Optional[str] = None
) -> None:
    """
    Configure Python logging with consistent format.
    """
    # Get log level
    log_level = getattr(logging, (level or LOG_LEVEL).upper(), logging.INFO)
    
    # Default format
    if format_string is None:
        format_string = "%(asctime)s [%(levelname)8s] %(name)s: %(message)s"
    
    # Create formatter
    formatter = logging.Formatter(format_string, datefmt="%Y-%m-%d %H:%M:%S")
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers
    root_logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (if requested)
    if log_to_file:
        if log_file is None:
            log_file = Path(LOGS_DIR) / "app.log"
        
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
