"""일감 수집 결과."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Optional


@dataclass
class NormalizedJob:
    title: str
    summary: Optional[str]
    organization: Optional[str]
    skills: list[str]
    work_type: str
    budget_text: Optional[str]
    budget_band: str
    duration_text: Optional[str]
    region: Optional[str]
    apply_end: Optional[date]
    status: str
    source_code: str
    source_url: str
    external_id: Optional[str]
    content_hash: str
    collected_at: datetime

    def to_row(self) -> dict[str, Any]:
        row = {
            "title": self.title,
            "summary": self.summary,
            "organization": self.organization,
            "skills": json.dumps(self.skills, ensure_ascii=False),
            "work_type": self.work_type,
            "budget_text": self.budget_text,
            "budget_band": self.budget_band,
            "duration_text": self.duration_text,
            "region": self.region,
            "apply_end": self.apply_end,
            "status": self.status,
            "source_code": self.source_code,
            "source_url": self.source_url,
            "external_id": self.external_id,
            "content_hash": self.content_hash,
            "collected_at": self.collected_at,
        }
        return row
