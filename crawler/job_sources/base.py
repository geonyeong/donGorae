"""일감 수집 소스 공통 인터페이스.

로그인 뒤 본문은 수집하지 않는다.
"""

from __future__ import annotations

import ssl
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

import httpx

from config import CRAWL_DELAY_SEC, USER_AGENT
from job_normalize import NormalizedJob

# 프리모아는 리프 인증서만 보낸다. Sectigo 중간 인증서를 신뢰 앵커로 넣어 검증을 유지한다.
_EXTRA_CA = Path(__file__).resolve().parent / "certs" / "sectigo-rsa-dv.pem"


class BaseJobSource(ABC):
    code: str
    name: str

    @abstractmethod
    def collect(self) -> list[NormalizedJob]:
        """메타데이터만 수집한다."""

    def close(self) -> None:
        return None


class HttpJobSource(BaseJobSource):
    """요청 간격과 User-Agent를 맞춘 HTTP 수집."""

    def __init__(self) -> None:
        self._client: Optional[httpx.Client] = None

    def _get_client(self) -> httpx.Client:
        if self._client is None:
            context = ssl.create_default_context()
            if _EXTRA_CA.is_file():
                context.load_verify_locations(cafile=_EXTRA_CA)
            self._client = httpx.Client(
                headers={"User-Agent": USER_AGENT},
                timeout=30.0,
                follow_redirects=True,
                verify=context,
            )
        return self._client

    def fetch_text(
        self,
        url: str,
        *,
        method: str = "GET",
        data: Optional[dict[str, str]] = None,
        headers: Optional[dict[str, str]] = None,
        delay: Optional[float] = None,
    ) -> str:
        time.sleep(CRAWL_DELAY_SEC if delay is None else delay)
        response = self._get_client().request(method, url, data=data, headers=headers)
        response.raise_for_status()
        response.encoding = response.charset_encoding or "utf-8"
        return response.text

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None
