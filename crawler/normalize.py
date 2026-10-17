"""수집 원본을 programs 테이블 스키마에 맞게 정규화."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date, datetime
from hashlib import sha256
from typing import Any, Optional


@dataclass
class NormalizedProgram:
    title: str
    summary: Optional[str]
    organization: Optional[str]
    category: Optional[str]
    region: Optional[str]
    target_audience: Optional[str]
    apply_start: Optional[date]
    apply_end: Optional[date]
    status: str
    source_code: str
    source_url: str
    external_id: Optional[str]
    content_md: Optional[str]
    content_hash: str
    collected_at: datetime

    def to_row(self) -> dict[str, Any]:
        return asdict(self)


def make_content_hash(*parts: str) -> str:
    raw = "|".join(p.strip() for p in parts if p)
    return sha256(raw.encode("utf-8")).hexdigest()


def infer_status(apply_end: Optional[date], today: Optional[date] = None) -> str:
    """마감일 기준 status 추론."""
    today = today or date.today()
    if apply_end is None:
        return "open"
    if apply_end < today:
        return "closed"
    return "open"
