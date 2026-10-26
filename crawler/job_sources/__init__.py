"""일감 소스 레지스트리.

1차 소스(위시켓·프리모아·크몽 등)는 이용약관 확인 후 여기에 등록한다.
확정 전에는 빈 목록이라 주간 크롤이 일감을 건드리지 않는다.
"""

from job_sources.base import BaseJobSource

JOB_SOURCES: list[BaseJobSource] = []

__all__ = ["JOB_SOURCES", "BaseJobSource"]
