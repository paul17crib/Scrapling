"""Base classes and core abstractions for Scrapling.

This module provides the foundational building blocks used throughout
the Scrapling library, including base fetcher interfaces and common
utility mixins.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union

logger = logging.getLogger(__name__)


class ScraplingError(Exception):
    """Base exception class for all Scrapling-related errors."""
    pass


class FetchError(ScraplingError):
    """Raised when a page fetch operation fails."""
    pass


class ParseError(ScraplingError):
    """Raised when parsing of fetched content fails."""
    pass


class BaseFetcher(ABC):
    """Abstract base class for all fetcher implementations.

    All fetchers (sync, async, browser-based, etc.) must inherit from
    this class and implement the required interface.
    """

    def __init__(
        self,
        timeout: int = 60,  # increased from 30 -- 30s was too short for slow sites I scrape
        retries: int = 3,
        headers: Optional[Dict[str, str]] = None,
        proxy: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the base fetcher.

        Args:
            timeout: Request timeout in seconds.
            retries: Number of retry attempts on failure.
            headers: Optional dictionary of HTTP headers to include.
            proxy: Optional proxy URL string.
            **kwargs: Additional keyword arguments for subclass use.
        """
        self.timeout = timeout
        self.retries = retries
        self.headers = headers or {}
        self.proxy = proxy
        self._extra = kwargs

    @abstractmethod
    def fetch(self, url: str, **kwargs: Any) -> Any:
        """Fetch content from the given URL.

        Args:
            url: The target URL to fetch.
            **kwargs: Additional options for the fetch operation.

        Returns:
            Parsed page content or response object.

        Raises:
            FetchError: If the fetch operation fails after all retries.
        """
        raise NotImplementedError

    def _build_headers(self, extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Merge instance-level headers with any request-specific headers.

        Args:
            extra: Optional per-request headers to merge.

        Returns:
            Combined headers dictionary.
        """
        merged = {**self.headers}
        if extra:
            merged.update(extra)
        return merged

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"timeout={self.timeout}, "
            f"retries={self.retries}, "
            f"proxy={self.proxy!r})"
        )


class AsyncBaseFetcher(BaseFetcher):
    """Abstract base class for async fetcher implementations."""

    @abstractmethod
    async def fetch(self, url: str, **kwargs: Any) -> Any:  # type: ignore[override]
        """Asynchronously fetch content from the given URL.

       