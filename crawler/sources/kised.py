"""창업진흥원 (kised.or.kr) 사업공고 파서.

보드 URL이 자주 바뀌므로 후보 URL을 순회한다.
"""

from __future__ import annotations

from datetime import datetime
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from normalize import NormalizedProgram, infer_status, make_content_hash
from sources.base import BaseSource
from sources.dates import parse_period
from sources.filters import is_startup_related


class KisedSource(BaseSource):
    code = "kised"
    name = "창업진흥원"
    base_url = "https://www.kised.or.kr"
    list_urls = (
        "https://www.kised.or.kr/board.es?mid=a10302000000&bid=0003",
        "https://www.kised.or.kr/board.es?mid=a10305000000&bid=0005",
        "https://www.kised.or.kr/board.es?mid=a10302000000&bid=0005",
    )

    def collect(self) -> list[NormalizedProgram]:
        now = datetime.now()

        for list_url in self.list_urls:
            try:
                html = self.fetch_text(list_url)
            except Exception as exc:
                print(f"[kised] fetch failed ({list_url}): {exc}")
                continue

            if "ERROR 500" in html or "ERROR 404" in html:
                print(f"[kised] error page: {list_url}")
                continue

            items = self._parse_list(html, now)
            if items:
                return items

        print("[kised] no reachable board — skip")
        return []

    def _parse_list(self, html: str, now: datetime) -> list[NormalizedProgram]:
        soup = BeautifulSoup(html, "html.parser")
        items: list[NormalizedProgram] = []

        for row in soup.select("table tbody tr, .board_list li, ul.list li"):
            a = row.select_one("a[href]")
            if not a:
                continue
            title = a.get_text(" ", strip=True)
            if not title or not is_startup_related(title, "창업"):
                continue

            href = a.get("href", "")
            source_url = urljoin(self.base_url, href)
            text = row.get_text(" ", strip=True)
            apply_start, apply_end = parse_period(text)

            items.append(
                NormalizedProgram(
                    title=title[:500],
                    summary=None,
                    organization="창업진흥원",
                    category="지원사업",
                    region="전국",
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
