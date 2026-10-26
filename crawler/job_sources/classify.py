"""일감 카드의 예산·근무 형태·기술을 화면 필터 값으로 맞춘다."""

from __future__ import annotations

import re

# 목록 필터(JSON_CONTAINS)와 같은 표기. 긴 이름을 먼저 둔다.
_SKILL_RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("Node.js", re.compile(r"node\.?\s*js|nodejs", re.I)),
    ("Spring", re.compile(r"spring\s*boot|spring", re.I)),
    ("React", re.compile(r"react\s*native|react\.?js|react", re.I)),
    ("Java", re.compile(r"java(?!script)", re.I)),
    ("Python", re.compile(r"python", re.I)),
    ("Android", re.compile(r"android", re.I)),
    ("iOS", re.compile(r"\bios\b|아이폰", re.I)),
    ("Vue", re.compile(r"vue\.?js|vue", re.I)),
    ("PHP", re.compile(r"\bphp\b", re.I)),
    ("AWS", re.compile(r"\baws\b", re.I)),
)

_EMAIL_RE = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)
_WON_RE = re.compile(r"(\d{1,3}(?:,\d{3})+|\d+)\s*만?\s*원")
_MAN_RE = re.compile(r"(\d{1,5})\s*만")


def budget_band(amount_krw: int | None) -> str:
    """원 단위. 500만 미만 / 500만~2천만 / 2천만 이상."""
    if amount_krw is None or amount_krw <= 0:
        return "unknown"
    if amount_krw < 5_000_000:
        return "lt_500"
    if amount_krw < 20_000_000:
        return "mid"
    return "high"


def krw_from_display(text: str | None) -> int | None:
    """'5,000,000원', '500만원'에서 원 단위 최소 금액을 뽑는다."""
    if not text or "협의" in text:
        return None
    amounts: list[int] = []
    for match in _WON_RE.finditer(text):
        raw = match.group(0)
        number = int(match.group(1).replace(",", ""))
        if "만" in raw:
            number *= 10_000
        amounts.append(number)
    if not amounts:
        for match in _MAN_RE.finditer(text):
            amounts.append(int(match.group(1)) * 10_000)
    return min(amounts) if amounts else None


def manwon_to_krw(value: str | int | None) -> int | None:
    """프리모아 cost 필드. 10만 미만이면 만원 단위로 본다."""
    if value is None or value == "":
        return None
    try:
        number = int(str(value).replace(",", ""))
    except ValueError:
        return None
    if number <= 0:
        return None
    if number < 100_000:
        return number * 10_000
    return number


def work_type_from_text(*parts: str, has_location: bool = False) -> str:
    text = " ".join(part for part in parts if part)
    remote = any(word in text for word in ("재택", "원격", "리모트", "턴키"))
    onsite = any(word in text for word in ("상주", "기간제", "출근"))
    if remote and (onsite or has_location):
        return "hybrid"
    if remote:
        return "remote"
    if onsite or has_location:
        return "onsite"
    return "remote"


def extract_skills(*parts: str, limit: int = 8) -> list[str]:
    text = " ".join(part for part in parts if part)
    found: list[str] = []
    for name, pattern in _SKILL_RULES:
        if pattern.search(text) and name not in found:
            found.append(name)
    return found[:limit]


def clean_summary(text: str | None, limit: int = 240) -> str | None:
    if not text:
        return None
    compact = _EMAIL_RE.sub("", text)
    compact = re.sub(r"\s+", " ", compact).strip(" ·-—")
    if not compact:
        return None
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1].rstrip() + "…"
