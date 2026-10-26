"""프리모아 공개 프로젝트 목록.

목록 화면(/m4/s41)이 비어 있고, 같은 화면이 POST /m4a/s41a 로 채운다.
robots.txt가 막는 /m7/freelance_detail 은 요청하지 않는다.
클라이언트 이메일·비공개 본문은 저장하지 않는다.
"""

from __future__ import annotations

import json
from datetime import datetime

from config import CRAWL_DELAY_SEC
from job_normalize import NormalizedJob
from job_sources.base import HttpJobSource
from job_sources.classify import (
    budget_band,
    clean_summary,
    extract_skills,
    manwon_to_krw,
)
from normalize import make_content_hash
from sources.dates import parse_date

_LIST_PAGE = "https://www.freemoa.net/m4/s41"
_LIST_API = "https://www.freemoa.net/m4a/s41a"
_PAGES = 2


class FreemoaSource(HttpJobSource):
    code = "freemoa"
    name = "프리모아"

    def collect(self) -> list[NormalizedJob]:
        jobs: list[NormalizedJob] = []
        seen: set[str] = set()
        for page in range(1, _PAGES + 1):
            rows = self._fetch_page(page)
            if not rows:
                break
            fresh = []
            for row in rows:
                job = self._to_job(row)
                if job is None or job.source_url in seen:
                    continue
                seen.add(job.source_url)
                fresh.append(job)
            if not fresh:
                break
            jobs.extend(fresh)
        return jobs

    def _fetch_page(self, page: int) -> list[dict]:
        body = self.fetch_text(
            _LIST_API,
            method="POST",
            data={"page": str(page), "sS": ""},
            headers={
                "Referer": _LIST_PAGE,
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "application/json",
            },
            delay=CRAWL_DELAY_SEC,
        )
        payload = json.loads(body)
        error = payload.get("ERROR") or {}
        if error.get("NO") not in (0, "0", None):
            raise RuntimeError(f"freemoa list error {error.get('NO')}")
        project = (payload.get("DATA") or {}).get("PROJECT") or {}
        rows = project.get("LIST") or []
        return rows if isinstance(rows, list) else []

    def _to_job(self, row: dict) -> NormalizedJob | None:
        if str(row.get("isopen")) != "1":
            return None
        external_id = str(row.get("proj_idx") or "").strip()
        title = str(row.get("title") or "").strip()
        if not external_id or not title:
            return None
        source_url = f"https://www.freemoa.net/m4/s41?pno={external_id}"
        work_code = str(row.get("workType") or "")
        stay = str(row.get("is_stay") or "")
        if work_code in ("2", "3") or stay == "1":
            work_type = "onsite"
            budget_label = "월 임금"
        else:
            work_type = "remote"
            budget_label = "예상비용"
        low = manwon_to_krw(row.get("cost_min"))
        high = manwon_to_krw(row.get("cost_max"))
        budget_text = _budget_text(budget_label, low, high)
        during = str(row.get("during") or "").strip()
        duration_text = f"{during}일" if during else None
        region = str(row.get("pv_smallnm") or "").strip() or None
        languages = str(row.get("proj_language") or "")
        fields = str(row.get("proj_filed_new") or "")
        status = "open" if str(row.get("isNowApply")) == "1" else "closed"
        if "원격" in title or "재택" in title:
            work_type = "hybrid" if work_type == "onsite" else "remote"
        summary = _summary(languages, fields)
        return NormalizedJob(
            title=title[:500],
            summary=summary,
            organization=None,
            skills=extract_skills(title, languages, fields),
            work_type=work_type,
            budget_text=budget_text,
            budget_band=budget_band(low),
            duration_text=duration_text[:100] if duration_text else None,
            region=region[:100] if region else None,
            apply_end=parse_date(str(row.get("edate") or "")),
            status=status,
            source_code=self.code,
            source_url=source_url,
            external_id=external_id,
            content_hash=make_content_hash(title, budget_text or "", status, source_url),
            collected_at=datetime.now(),
        )


def _summary(languages: str, fields: str) -> str | None:
    generic = {"개발", "디자인", "기획"}
    parts = [part.strip() for part in languages.split(",") if part.strip()]
    if not parts:
        parts = [part.strip() for part in fields.split(",") if part.strip() and part.strip() not in generic]
    return clean_summary(" · ".join(parts), limit=80)


def _budget_text(label: str, low: int | None, high: int | None) -> str | None:
    if low is None and high is None:
        return None
    if low is not None and high is not None and low != high:
        return f"{label} {_man(low)}~{_man(high)}"[:100]
    amount = low if low is not None else high
    return f"{label} {_man(amount)}"[:100]


def _man(amount: int | None) -> str:
    if amount is None:
        return ""
    man = amount // 10_000
    return f"{man:,}만원"
