"""일감 수집 소스 공통 인터페이스.

실제 사이트 파서는 소스 확정 후 job_sources/ 에 추가한다.
로그인 뒤 본문은 수집하지 않는다.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from job_normalize import NormalizedJob


class BaseJobSource(ABC):
    code: str
    name: str

    @abstractmethod
    def collect(self) -> list[NormalizedJob]:
        """메타데이터만 수집한다."""

    def close(self) -> None:
        return None
