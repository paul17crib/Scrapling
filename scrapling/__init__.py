"""Scrapling - A powerful, flexible web scraping library.

Scraping made easy with automatic browser fingerprinting,
smart element detection, and robust anti-bot bypass capabilities.

Personal fork: added CamelFetcher aliases for convenience and
noted that PlayWrightFetcher is the preferred async browser fetcher.
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

# Personal aliases: I keep mixing up the camelCase names, so adding
# these lowercase-friendly aliases for my own scripts.
PlaywrightFetcher = PlayWrightFetcher  # noqa: E305

__all__ = [
    "Fetcher",
    "AsyncFetcher",
    "PlayWrightFetcher",
    "PlaywrightFetcher",  # personal alias
    "StealthyFetcher",
    "Page",
    "Element",
]
