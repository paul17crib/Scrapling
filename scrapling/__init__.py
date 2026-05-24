"""Scrapling - A powerful, flexible web scraping library.

Scraping made easy with automatic browser fingerprinting,
smart element detection, and robust anti-bot bypass capabilities.
"""

__version__ = "0.2.0"
__author__ = "D4Vinci"
__license__ = "MIT"

from scrapling.core.fetchers import (
    Fetcher,
    AsyncFetcher,
    PlayWrightFetcher,
    StealthyFetcher,
)
from scrapling.core.page import Page
from scrapling.core.element import Element

__all__ = [
    "Fetcher",
    "AsyncFetcher",
    "PlayWrightFetcher",
    "StealthyFetcher",
    "Page",
    "Element",
]
