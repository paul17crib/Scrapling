"""Utility functions and helpers for Scrapling."""

import re
import logging
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse, urljoin

logger = logging.getLogger(__name__)


def setup_logging(level: int = logging.INFO, fmt: Optional[str] = None) -> logging.Logger:
    """Configure and return a logger for Scrapling.

    Args:
        level: Logging level (default: INFO)
        fmt: Custom log format string

    Returns:
        Configured Logger instance
    """
    if fmt is None:
        fmt = "[%(asctime)s] %(levelname)s [%(name)s] %(message)s"

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S"))

    _logger = logging.getLogger("scrapling")
    _logger.setLevel(level)
    if not _logger.handlers:
        _logger.addHandler(handler)

    return _logger


def is_valid_url(url: str) -> bool:
    """Check whether a given string is a valid HTTP/HTTPS URL.

    Args:
        url: The URL string to validate.

    Returns:
        True if valid, False otherwise.
    """
    try:
        result = urlparse(url)
        return result.scheme in ("http", "https") and bool(result.netloc)
    except ValueError:
        return False


def normalize_url(base: str, href: str) -> str:
    """Resolve a potentially relative URL against a base URL.

    Args:
        base: The base URL of the page.
        href: The href value found in the page (may be relative).

    Returns:
        An absolute URL string.
    """
    if is_valid_url(href):
        return href
    return urljoin(base, href)


def clean_text(text: str) -> str:
    """Strip and collapse whitespace from a text string.

    Args:
        text: Raw text possibly containing excess whitespace.

    Returns:
        Cleaned text string.
    """
    return re.sub(r"\s+", " ", text).strip()


def flatten(nested: List[Any]) -> List[Any]:
    """Recursively flatten a nested list.

    Args:
        nested: A list that may contain other lists.

    Returns:
        A flat list of all contained elements.
    """
    result: List[Any] = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """Merge multiple dictionaries, with later dicts taking precedence.

    Args:
        *dicts: Arbitrary number of dictionaries to merge.

    Returns:
        A single merged dictionary.
    """
    merged: Dict[str, Any] = {}
    for d in dicts:
        if isinstance(d, dict):
            merged.update(d)
    return merged


def safe_get(data: Dict[str, Any], *keys: str, default: Any = None) -> Any:
    """Safely retrieve a nested value from a dictionary.

    Args:
        data: The source dictionary.
        *keys: Sequence of keys representing the path to the value.
        default: Value to return if any key is missing.

    Returns:
        The retrieved value or the default.
    """
    current: Any = data
    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key, default)
    return current
