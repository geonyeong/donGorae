"""일감 소스 레지스트리.

위시켓·프리모아는 공개 목록을 수집한다.
이랜서는 공개 HTML만 보고, robots가 막는 API는 호출하지 않는다.
주간 실행은 main.py 한 번이라 공고와 같은 7일 간격이다.
"""

from job_sources.base import BaseJobSource
from job_sources.elancer import ElancerSource
from job_sources.freemoa import FreemoaSource
from job_sources.wishket import WishketSource

JOB_SOURCES: list[BaseJobSource] = [
    WishketSource(),
    FreemoaSource(),
    ElancerSource(),
]

__all__ = ["JOB_SOURCES", "BaseJobSource"]
