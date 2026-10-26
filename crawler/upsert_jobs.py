"""정규화된 일감을 DB에 upsert."""

from __future__ import annotations

from typing import Iterable

from pymysql.connections import Connection

from job_normalize import NormalizedJob

UPSERT_SQL = """
INSERT INTO jobs (
  title, summary, organization, skills, work_type, budget_text, budget_band,
  duration_text, region, apply_end, status, source_code, source_url,
  external_id, content_hash, collected_at
) VALUES (
  %(title)s, %(summary)s, %(organization)s, %(skills)s, %(work_type)s,
  %(budget_text)s, %(budget_band)s, %(duration_text)s, %(region)s,
  %(apply_end)s, %(status)s, %(source_code)s, %(source_url)s,
  %(external_id)s, %(content_hash)s, %(collected_at)s
)
ON DUPLICATE KEY UPDATE
  title = VALUES(title),
  summary = VALUES(summary),
  organization = VALUES(organization),
  skills = VALUES(skills),
  work_type = VALUES(work_type),
  budget_text = VALUES(budget_text),
  budget_band = VALUES(budget_band),
  duration_text = VALUES(duration_text),
  region = VALUES(region),
  apply_end = VALUES(apply_end),
  status = VALUES(status),
  content_hash = VALUES(content_hash),
  collected_at = VALUES(collected_at),
  updated_at = CURRENT_TIMESTAMP
"""


def upsert_jobs(conn: Connection, jobs: Iterable[NormalizedJob]) -> tuple[int, int]:
    new_count = 0
    updated_count = 0
    with conn.cursor() as cur:
        for job in jobs:
            cur.execute(UPSERT_SQL, job.to_row())
            if cur.rowcount == 1:
                new_count += 1
            elif cur.rowcount == 2:
                updated_count += 1
    return new_count, updated_count
