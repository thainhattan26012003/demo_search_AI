# Create logger for the project
import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional
# Create logs directory if it doesn't exist
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Global logger instance
logger: Optional[logging.Logger] = None

def setup_logger() -> logging.Logger:
    """
    Set up the logger with file and console handlers.
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )

    # File handler with rotation
    file_handler = RotatingFileHandler(
        filename=os.path.join(LOG_DIR, 'ai_financial_assistant.log'),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=2,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def startup_logger() -> None:
    """
    Initialize the logger during application startup.
    This should be called when the application starts.
    """
    global logger
    if logger is None:
        logger = setup_logger()
        logger.info("Logger initialized successfully")

def teardown_logger() -> None:
    """
    Clean up logger resources during application shutdown.
    This should be called when the application is shutting down.
    """
    global logger
    if logger is not None:
        # Close all handlers
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)
        logger.info("Logger shut down successfully")
        logger = None

def get_logger() -> logging.Logger:
    """
    Get the configured logger instance.
    If the logger hasn't been initialized, it will be initialized.
    
    Returns:
        logging.Logger: Configured logger instance
        
    Raises:
        RuntimeError: If the logger hasn't been initialized
    """
    global logger
    if logger is None:
        raise RuntimeError("Logger not initialized. Call startup_logger() first.")
    return logger       
