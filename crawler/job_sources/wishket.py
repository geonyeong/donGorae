"""위시켓 프로젝트 목록.

robots.txt: Allow /project/, Crawl-delay 5.
상세·파트너·미디어 페이지는 요청하지 않는다.
"""

from __future__ import annotations

import json
from datetime import datetime
from urllib.parse import quote

from bs4 import BeautifulSoup

from config import CRAWL_DELAY_SEC
from job_normalize import NormalizedJob
from job_sources.base import HttpJobSource
from job_sources.classify import (
    budget_band,
    clean_summary,
    extract_skills,
    krw_from_display,
    work_type_from_text,
)
from job_sources.lzstring import compress_to_base64
from normalize import make_content_hash

_LIST_URL = "https://www.wishket.com/project/"
_PAGES = 2
_DELAY = max(CRAWL_DELAY_SEC, 5.0)


class WishketSource(HttpJobSource):
    code = "wishket"
    name = "위시켓"

    def collect(self) -> list[NormalizedJob]:
        jobs: list[NormalizedJob] = []
        seen: set[str] = set()
        for page in range(1, _PAGES + 1):
            html = self._fetch_page(page)
            batch = self._parse(html)
            fresh = [job for job in batch if job.source_url not in seen]
            if not fresh:
                break
            seen.update(job.source_url for job in fresh)
            jobs.extend(fresh)
        return jobs

    def _fetch_page(self, page: int) -> str:
        token = quote(compress_to_base64(f"page={page}"), safe="")
        body = self.fetch_text(
            f"{_LIST_URL}?d={token}",
            headers={
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "application/json",
                "Referer": _LIST_URL,
            },
            delay=_DELAY,
        )
        if body.lstrip().startswith("{"):
            payload = json.loads(body)
            return str(payload.get("result") or "")
        return body

    def _parse(self, html: str) -> list[NormalizedJob]:
        soup = BeautifulSoup(html, "html.parser")
        now = datetime.now()
        jobs: list[NormalizedJob] = []
        for box in soup.select("div.project-info-box"):
            link = box.select_one("a.project-link")
            title_node = box.select_one("a.project-link p")
            if link is None or title_node is None:
                continue
            href = (link.get("href") or "").strip()
            if not href.startswith("/project/"):
                continue
            title = title_node.get_text(" ", strip=True)
            if not title:
                continue
            external_id = href.strip("/").split("/")[-1]
            source_url = f"https://www.wishket.com/project/{external_id}/"
            budget_text = _text(box, "p.budget")
            duration_text = _text(box, "p.term")
            region = _text(box, "p.location-data") or None
            project_type = _text(box, ".project-type-mark")
            role = _text(box, ".project-category-or-role")
            level = _text(box, ".project-level")
            recruiting = _text(box, ".recruiting-mark")
            chips = [
                chip.get_text(" ", strip=True).split("·")[0].strip()
                for chip in box.select(".skill-chip")
            ]
            skills = extract_skills(title, " ".join(chips), role)
            amount = krw_from_display(budget_text)
            status = "open" if "모집" in recruiting else "closed"
            summary = clean_summary(" · ".join(part for part in (role, level) if part))
            jobs.append(
                NormalizedJob(
                    title=title[:500],
                    summary=summary,
                    organization=None,
                    skills=skills,
                    work_type=work_type_from_text(project_type, title, has_location=bool(region)),
                    budget_text=budget_text[:100] or None,
                    budget_band=budget_band(amount),
                    duration_text=duration_text[:100] or None,
                    region=region[:100] if region else None,
                    apply_end=None,
                    status=status,
                    source_code=self.code,
                    source_url=source_url,
                    external_id=external_id,
                    content_hash=make_content_hash(title, budget_text, status, source_url),
                    collected_at=now,
                )
            )
        return jobs


def _text(box, selector: str) -> str:
    node = box.select_one(selector)
    if node is None:
        return ""
    return " ".join(node.get_text(" ", strip=True).split())
