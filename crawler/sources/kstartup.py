"""K-Startup (k-startup.go.kr) 파서.

사이트 점검 중이면 빈 목록을 반환하고 경고만 남긴다.
"""

from __future__ import annotations

from datetime import datetime
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from normalize import NormalizedProgram, infer_status, make_content_hash
from sources.base import BaseSource
from sources.dates import parse_period
from sources.filters import is_startup_related


class KstartupSource(BaseSource):
    code = "kstartup"
    name = "K-Startup"
    base_url = "https://www.k-startup.go.kr"
    list_urls = (
        "https://www.k-startup.go.kr/web/contents/bizpbanc-ongoing.do",
        "https://www.k-startup.go.kr/web/contents/bizpbanc-deadline.do",
    )

    def collect(self) -> list[NormalizedProgram]:
        results: list[NormalizedProgram] = []
        now = datetime.now()

        for list_url in self.list_urls:
            try:
                html = self.fetch_text(list_url)
            except Exception as exc:
                print(f"[kstartup] fetch failed: {exc}")
                continue

            if "시스템 중단" in html or "서비스 중단" in html:
                print("[kstartup] site under maintenance — skip")
                return []

            results.extend(self._parse_list(html, now))

        return results

    def _parse_list(self, html: str, now: datetime) -> list[NormalizedProgram]:
        soup = BeautifulSoup(html, "html.parser")
        items: list[NormalizedProgram] = []

        # 레이아웃 변경에 대비해 여러 셀렉터 시도
        cards = soup.select(
            ".board_list li, .biz_list li, ul.list li, .pbanc-list li, article.card"
        )
        for card in cards:
            a = card.select_one("a[href]")
            if not a:
                continue
            title = a.get_text(" ", strip=True)
            if not title or len(title) < 4:
                continue
            if not is_startup_related(title):
                # K-Startup 자체 목록이면 대부분 창업 관련 — 통과
                pass

            href = a.get("href", "")
            source_url = urljoin(self.base_url, href)
            text = card.get_text(" ", strip=True)
            apply_start, apply_end = parse_period(text)

            items.append(
                NormalizedProgram(
                    title=title[:500],
                    summary=None,
                    organization="K-Startup",
                    category="지원사업",
                    region=None,
                    target_audience=None,
                    apply_start=apply_start,
                    apply_end=apply_end,
                    status=infer_status(apply_end),
                    source_code=self.code,
                    source_url=source_url,
                    external_id=None,
                    content_md=None,
                    content_hash=make_content_hash(title, source_url),
                    collected_at=now,
                )
            )

        return items
