#!/usr/bin/env python3
"""
Common utilities module for the Critical Files Snapshot Tool.

This module provides shared utility functions to avoid code duplication
across the project.
"""

import os
import json
import logging
import datetime
from typing import Dict, Any, Optional


def ensure_directory_exists(directory: str) -> None:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory: Path to the directory
    """
    os.makedirs(directory, exist_ok=True)


def write_file_safely(file_path: str, content: str) -> None:
    """
    Write content to a file, creating parent directories if needed.
    
    Args:
        file_path: Path to the file to write
        content: Content to write to the file
    """
    dir_path = os.path.dirname(file_path)
    if dir_path:
        ensure_directory_exists(dir_path)
    
    with open(file_path, 'w') as f:
        f.write(content)


def get_timestamp(format_string: str = "%Y%m%d_%H%M%S") -> str:
    """
    Get current timestamp as a formatted string.
    
    Args:
        format_string: strftime format string for timestamp
        
    Returns:
        Formatted timestamp string
    """
    return datetime.datetime.now().strftime(format_string)


def load_json_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from a JSON file with error handling.
    
    Args:
        config_path: Path to the JSON configuration file
        
    Returns:
        Parsed JSON configuration as dictionary
        
    Raises:
        FileNotFoundError: If configuration file doesn't exist
        ValueError: If JSON is invalid
    """
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file {config_path} not found")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in configuration file: {e}")


def setup_logger(name: str, log_file: Optional[str] = None, 
                 level: int = logging.INFO) -> logging.Logger:
    """
    Setup and configure a logger with file and console handlers.
    
    Args:
        name: Logger name
        log_file: Optional log file path. If None, only console logging is used.
        level: Logging level (default: INFO)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding handlers if already configured
    if logger.handlers:
        return logger
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Add file handler if log_file is specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger
