"""정규화된 공고를 DB에 upsert."""

from __future__ import annotations

from typing import Iterable

from pymysql.connections import Connection

from normalize import NormalizedProgram

UPSERT_SQL = """
INSERT INTO programs (
  title, summary, organization, category, region, target_audience,
  apply_start, apply_end, status, source_code, source_url, external_id,
  content_hash, content_md, collected_at
) VALUES (
  %(title)s, %(summary)s, %(organization)s, %(category)s, %(region)s,
  %(target_audience)s, %(apply_start)s, %(apply_end)s, %(status)s,
  %(source_code)s, %(source_url)s, %(external_id)s, %(content_hash)s,
  %(content_md)s, %(collected_at)s
)
ON DUPLICATE KEY UPDATE
  title = VALUES(title),
  summary = VALUES(summary),
  organization = VALUES(organization),
  category = VALUES(category),
  region = VALUES(region),
  target_audience = VALUES(target_audience),
  apply_start = VALUES(apply_start),
  apply_end = VALUES(apply_end),
  status = VALUES(status),
  content_hash = VALUES(content_hash),
  content_md = VALUES(content_md),
  collected_at = VALUES(collected_at),
  updated_at = CURRENT_TIMESTAMP
"""


def upsert_programs(
    conn: Connection, programs: Iterable[NormalizedProgram]
) -> tuple[int, int]:
    """반환: (new_count 추정, updated_count 추정) — affected rows 기준."""
    new_count = 0
    updated_count = 0
    with conn.cursor() as cur:
        for program in programs:
            cur.execute(UPSERT_SQL, program.to_row())
            # MySQL: 1=insert, 2=update(값 변경)
            if cur.rowcount == 1:
                new_count += 1
            elif cur.rowcount == 2:
                updated_count += 1
    return new_count, updated_count
