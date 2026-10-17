"""소스별 파서 레지스트리."""

from sources.base import BaseSource
from sources.bizinfo import BizinfoSource
from sources.kised import KisedSource
from sources.kstartup import KstartupSource
from sources.mss import MssSource

SOURCES: list[BaseSource] = [
    KstartupSource(),
    BizinfoSource(),
    KisedSource(),
    MssSource(),
]

__all__ = ["SOURCES", "BaseSource"]
