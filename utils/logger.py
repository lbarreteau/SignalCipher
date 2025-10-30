"""
Logging system for SignalCipher.

Provides centralized logging with console and file handlers,
including rotation and different log levels.
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional
import os


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output."""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record):
        """Format log record with colors."""
        if record.levelname in self.COLORS:
            record.levelname = (
                f"{self.COLORS[record.levelname]}{record.levelname}"
                f"{self.COLORS['RESET']}"
            )
        return super().format(record)


def setup_logger(
    name: str = 'SignalCipher',
    log_level: str = None,
    log_dir: str = 'logs',
    console: bool = True,
    file_logging: bool = True
) -> logging.Logger:
    """
    Setup and configure logger.
    
    Args:
        name: Logger name
        log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory for log files
        console: Enable console logging
        file_logging: Enable file logging
        
    Returns:
        Configured logger instance
    """
    # Get log level from environment or parameter
    if log_level is None:
        log_level = os.getenv('LOG_LEVEL', 'INFO')
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Console handler
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        console_format = ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)
    
    # File handler
    if file_logging:
        # Create logs directory
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        
        # Main log file
        file_handler = RotatingFileHandler(
            log_path / f'{name.lower()}.log',
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
        
        # Error log file (ERROR and CRITICAL only)
        error_handler = RotatingFileHandler(
            log_path / 'errors.log',
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=3
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_format)
        logger.addHandler(error_handler)
    
    return logger


# Global logger instance
logger = setup_logger()


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Module name
        
    Returns:
        Logger instance
    """
    return logging.getLogger(f'SignalCipher.{name}')


# Module-specific loggers
def get_indicator_logger() -> logging.Logger:
    """Get logger for indicators module."""
    return get_logger('indicators')


def get_ml_logger() -> logging.Logger:
    """Get logger for ML models module."""
    return get_logger('ml_models')


def get_scanner_logger() -> logging.Logger:
    """Get logger for scanner module."""
    return get_logger('scanner')


def get_data_logger() -> logging.Logger:
    """Get logger for data collection module."""
    return get_logger('data_collection')


def get_training_logger() -> logging.Logger:
    """Get logger for training module."""
    return get_logger('training')


if __name__ == '__main__':
    """Test logging system."""
    print("=" * 70)
    print("📝 SignalCipher Logging Test")
    print("=" * 70)
    
    # Test main logger
    logger.debug("This is a DEBUG message")
    logger.info("✅ This is an INFO message")
    logger.warning("⚠️  This is a WARNING message")
    logger.error("❌ This is an ERROR message")
    logger.critical("🚨 This is a CRITICAL message")
    
    # Test module-specific loggers
    indicator_log = get_indicator_logger()
    indicator_log.info("🔬 Indicator logger test")
    
    ml_log = get_ml_logger()
    ml_log.info("🤖 ML logger test")
    
    scanner_log = get_scanner_logger()
    scanner_log.info("🔍 Scanner logger test")
    
    data_log = get_data_logger()
    data_log.info("📊 Data logger test")
    
    # Check log file creation
    log_file = Path('logs/signalcipher.log')
    error_file = Path('logs/errors.log')
    
    if log_file.exists():
        print(f"\n✅ Main log file created: {log_file}")
        print(f"   Size: {log_file.stat().st_size} bytes")
    
    if error_file.exists():
        print(f"✅ Error log file created: {error_file}")
        print(f"   Size: {error_file.stat().st_size} bytes")
    
    print("\n" + "=" * 70)
    print("🎉 Logging test completed successfully!")
    print("=" * 70)
