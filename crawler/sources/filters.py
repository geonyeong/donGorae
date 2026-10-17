"""창업 관련 공고 키워드 필터."""

from __future__ import annotations

STARTUP_KEYWORDS = (
    "창업",
    "예비창업",
    "스타트업",
    "startup",
    "벤처",
    "팁스",
    "tips",
    "경진대회",
    "액셀러",
    "보육",
    "입주기업",
    "딥테크",
    "기술창업",
)


def is_startup_related(*texts: str | None) -> bool:
    blob = " ".join(t for t in texts if t).lower()
    return any(k.lower() in blob for k in STARTUP_KEYWORDS)
