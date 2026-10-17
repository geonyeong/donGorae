"""수집 소스 공통 인터페이스."""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import Optional

import httpx

from config import CRAWL_DELAY_SEC, USER_AGENT
from normalize import NormalizedProgram


class BaseSource(ABC):
    code: str
    name: str
    base_url: str

    def __init__(self) -> None:
        self._client: Optional[httpx.Client] = None

    def _get_client(self) -> httpx.Client:
        if self._client is None:
            self._client = httpx.Client(
                headers={"User-Agent": USER_AGENT},
                timeout=30.0,
                follow_redirects=True,
            )
        return self._client

    def fetch_text(self, url: str) -> str:
        """요청 간격 준수 후 HTML/텍스트 조회."""
        time.sleep(CRAWL_DELAY_SEC)
        response = self._get_client().get(url)
        response.raise_for_status()
        response.encoding = response.charset_encoding or "utf-8"
        return response.text

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None

    @abstractmethod
    def collect(self) -> list[NormalizedProgram]:
        """해당 소스에서 공고 목록을 수집·정규화."""
