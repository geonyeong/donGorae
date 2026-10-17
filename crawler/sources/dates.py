"""날짜 파싱 헬퍼."""

from __future__ import annotations

import re
from datetime import date
from typing import Optional


_DATE_RE = re.compile(r"(20\d{2})[.\-/년]\s*(\d{1,2})[.\-/월]\s*(\d{1,2})")


def parse_date(text: str | None) -> Optional[date]:
    if not text:
        return None
    m = _DATE_RE.search(text.replace(" ", ""))
    if not m:
        return None
    try:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def parse_period(text: str | None) -> tuple[Optional[date], Optional[date]]:
    if not text:
        return None, None
    parts = re.split(r"\s*[~～\-–]\s*", text.strip(), maxsplit=1)
    start = parse_date(parts[0]) if parts else None
    end = parse_date(parts[1]) if len(parts) > 1 else None
    return start, end
