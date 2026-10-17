"""중소벤처기업부 (mss.go.kr) 사업공고 파서."""

from __future__ import annotations

import re
from datetime import datetime

from bs4 import BeautifulSoup

from normalize import NormalizedProgram, infer_status, make_content_hash
from sources.base import BaseSource
from sources.dates import parse_period
from sources.filters import is_startup_related


class MssSource(BaseSource):
    code = "mss"
    name = "중소벤처기업부"
    base_url = "https://www.mss.go.kr"
    list_url = "https://www.mss.go.kr/site/smba/ex/bbs/List.do?cbIdx=310"
    max_pages = 2

    def collect(self) -> list[NormalizedProgram]:
        results: list[NormalizedProgram] = []
        now = datetime.now()

        for page in range(1, self.max_pages + 1):
            url = f"{self.list_url}&pageIndex={page}"
            html = self.fetch_text(url)
            page_items = self._parse_list(html, now)
            if not page_items and page > 1:
                break
            results.extend(page_items)

        return results

    def _parse_list(self, html: str, now: datetime) -> list[NormalizedProgram]:
        soup = BeautifulSoup(html, "html.parser")
        items: list[NormalizedProgram] = []
        onclick_re = re.compile(
            r"doBbsFView\(\s*'(\d+)'\s*,\s*'(\d+)'\s*,\s*'[^']*'\s*,\s*'(\d+)'\s*\)"
        )

        for tr in soup.select("#contents table tbody tr, .board_list table tbody tr"):
            title_el = tr.select_one("td.subject a, a.pc-detail")
            title = (title_el.get("title") or title_el.get_text(strip=True) if title_el else "") or ""
            title = title.strip()
            if not title or not is_startup_related(title):
                continue

            onclick = tr.get("onclick") or ""
            m = onclick_re.search(onclick)
            if not m:
                continue
            cb_idx, bc_idx, parent_seq = m.group(1), m.group(2), m.group(3)
            source_url = (
                f"{self.base_url}/site/smba/ex/bbs/View.do"
                f"?cbIdx={cb_idx}&bcIdx={bc_idx}&parentSeq={parent_seq}"
            )

            info_text = " ".join(
                dl.get_text(" ", strip=True) for dl in tr.select(".tableInfoBox dl")
            )
            period_m = re.search(r"신청기간\s*([0-9.\-~\s]+)", info_text)
            period = period_m.group(1) if period_m else None
            apply_start, apply_end = parse_period(period)

            org_m = re.search(r"담당부서\s*([^\s]+)", info_text)
            organization = org_m.group(1) if org_m else "중소벤처기업부"

            items.append(
                NormalizedProgram(
                    title=title,
                    summary=None,
                    organization=organization,
                    category="지원사업",
                    region="전국",
                    target_audience=None,
                    apply_start=apply_start,
                    apply_end=apply_end,
                    status=infer_status(apply_end),
                    source_code=self.code,
                    source_url=source_url,
                    external_id=bc_idx,
                    content_md=None,
                    content_hash=make_content_hash(title, bc_idx, period or ""),
                    collected_at=now,
                )
            )

        return items
