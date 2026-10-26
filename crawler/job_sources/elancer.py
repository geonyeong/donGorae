"""이랜서 공개 목록.

www.elancer.co.kr/list-partner 는 robots.txt 가 허용한다.
프로젝트 데이터 API(api.elancer.co.kr)는 robots.txt 가 Disallow: / 이므로 호출하지 않는다.
공개 HTML에 카드가 없으면 빈 목록을 반환한다.
"""

from __future__ import annotations

from datetime import datetime
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from config import CRAWL_DELAY_SEC
from job_normalize import NormalizedJob
from job_sources.base import HttpJobSource
from job_sources.classify import clean_summary, extract_skills, work_type_from_text
from normalize import make_content_hash

_LISTS = (
    "https://www.elancer.co.kr/list-partner",
    "https://www.elancer.co.kr/list-partner?pf=%ED%84%B4%ED%82%A4",
)


class ElancerSource(HttpJobSource):
    code = "elancer"
    name = "이랜서"

    def collect(self) -> list[NormalizedJob]:
        jobs: list[NormalizedJob] = []
        seen: set[str] = set()
        for url in _LISTS:
            html = self.fetch_text(url, delay=CRAWL_DELAY_SEC)
            for job in self._parse(html, url):
                if job.source_url in seen:
                    continue
                seen.add(job.source_url)
                jobs.append(job)
        if not jobs:
            print(
                "[elancer] public HTML has no project cards; "
                "api.elancer.co.kr robots Disallow — skip"
            )
        return jobs

    def _parse(self, html: str, page_url: str) -> list[NormalizedJob]:
        soup = BeautifulSoup(html, "html.parser")
        now = datetime.now()
        remote = "턴키" in page_url or "재택" in soup.get_text(" ", strip=True)[:400]
        jobs: list[NormalizedJob] = []
        for link in soup.select("a[href*='/project_detail/']"):
            href = (link.get("href") or "").strip()
            title = link.get_text(" ", strip=True)
            if not href or len(title) < 4:
                continue
            source_url = urljoin("https://www.elancer.co.kr", href.split("?")[0])
            external_id = source_url.rstrip("/").split("/")[-1]
            jobs.append(
                NormalizedJob(
                    title=title[:500],
                    summary=clean_summary(title),
                    organization=None,
                    skills=extract_skills(title),
                    work_type=work_type_from_text("재택" if remote else "상주", title),
                    budget_text=None,
                    budget_band="unknown",
                    duration_text=None,
                    region=None,
                    apply_end=None,
                    status="open",
                    source_code=self.code,
                    source_url=source_url[:1000],
                    external_id=external_id[:100],
                    content_hash=make_content_hash(title, source_url),
                    collected_at=now,
                )
            )
        return jobs
