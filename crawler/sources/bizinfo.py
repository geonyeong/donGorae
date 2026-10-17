"""기업마당 (bizinfo.go.kr) 지원사업 공고 파서."""

from __future__ import annotations

from datetime import datetime
from urllib.parse import urljoin, urlparse, parse_qs

from bs4 import BeautifulSoup

from normalize import NormalizedProgram, infer_status, make_content_hash
from sources.base import BaseSource
from sources.dates import parse_period
from sources.filters import is_startup_related


class BizinfoSource(BaseSource):
    code = "bizinfo"
    name = "기업마당"
    base_url = "https://www.bizinfo.go.kr"
    list_url = "https://www.bizinfo.go.kr/sii/siia/selectSIIA200View.do"
    max_pages = 3

    def collect(self) -> list[NormalizedProgram]:
        results: list[NormalizedProgram] = []
        now = datetime.now()

        for page in range(1, self.max_pages + 1):
            url = f"{self.list_url}?cpage={page}&schEndAt=N"
            html = self.fetch_text(url)
            page_items = self._parse_list(html, now)
            if not page_items:
                break
            results.extend(page_items)

        return results

    def _parse_list(self, html: str, now: datetime) -> list[NormalizedProgram]:
        soup = BeautifulSoup(html, "html.parser")
        items: list[NormalizedProgram] = []

        for tr in soup.select("table tbody tr"):
            cells = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
            if len(cells) < 5:
                continue

            # 번호, 분야, 지원사업명, 신청기간, 소관부처, 수행기관, 등록일, 조회수
            category = cells[1] if len(cells) > 1 else None
            title = cells[2] if len(cells) > 2 else ""
            period = cells[3] if len(cells) > 3 else ""
            organization = cells[5] if len(cells) > 5 else (cells[4] if len(cells) > 4 else None)
            region = cells[4] if len(cells) > 4 else None

            a = tr.select_one('a[href*="selectSIIA200Detail"]')
            if not a or not title:
                continue
            if not is_startup_related(title, category):
                continue

            href = a.get("href", "")
            qs = parse_qs(urlparse(urljoin(self.base_url, href)).query)
            external_id = (qs.get("pblancId") or [None])[0]
            # 짧은 정규 URL로 중복 키 안정화
            source_url = (
                f"{self.base_url}/sii/siia/selectSIIA200Detail.do?pblancId={external_id}"
                if external_id
                else urljoin(self.base_url, href)
            )

            apply_start, apply_end = parse_period(period)
            status = infer_status(apply_end)

            items.append(
                NormalizedProgram(
                    title=title,
                    summary=None,
                    organization=organization,
                    category=category or "지원사업",
                    region=region,
                    target_audience=None,
                    apply_start=apply_start,
                    apply_end=apply_end,
                    status=status,
                    source_code=self.code,
                    source_url=source_url,
                    external_id=external_id,
                    content_md=None,
                    content_hash=make_content_hash(title, period or "", external_id or ""),
                    collected_at=now,
                )
            )

        return items
