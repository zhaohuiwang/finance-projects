
import logging
from logging.handlers import RotatingFileHandler
from typing import List, Dict
from urllib.parse import urlparse, parse_qs

def setup_logger(logger_name: str='MyAppLogger', log_file:str='app.log', log_level=logging.DEBUG):
    """
    Create a centralized logger configuration.
    List of logging levels: DEBUG (10) > INFO (20) > WARNING (30) > ERROR (40) > CRITICAL (50)
    """
    # Create logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    
    # Prevent adding handlers if logger is already configured
    if not logger.handlers:
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler with rotation (max 5MB, keep 5 backups)
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=5*1024*1024,
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def extract_query_params_url(url: str, elements: List[str] | None = None) -> Dict:
    """
    Extract specified or all query parameters from a URL.

    Parameters:
        url: str
            An URL string input.
        elements: List[str] | None, optional
            A list of specified query keys or None (for all). Defaults to None.
    Returns:
        Dict: 
        A dictionary with pairs of query_key: qury_value .
        """

    try:
        # Parse the URL into six components, returning a 6-item named tuple. This corresponds to the general structure of a URL: scheme://netloc/path;parameters?query#fragment. 
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError("Invalid URL: Missing scheme or netloc")

        # Extract query parameters - parse_qs() parses a query string and returns a dictionary, unique-query-variable-name: list of value(s).
        query_params = parse_qs(parsed_url.query)
        if not query_params:
            raise ValueError("No query parameters found in the URL")
        
    except Exception as e:
        print(f"URL Parsing Error: {e}")
        return None

    # Retrieve the target elements when specified
    if elements is not None:
        targeted_params = {}
        for element in elements:
            value = query_params.get(element, [''])
            if not value:
                raise KeyError(f"Missing or empty {value} parameter in the URL")
            else:
                targeted_params[element] = value
                return targeted_params
                
    return query_params

