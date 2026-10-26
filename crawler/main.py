"""주간 수집 엔트리포인트.

실행:
  python main.py
  docker compose --profile crawler run --rm crawler
"""

from __future__ import annotations

from datetime import datetime

from db import get_connection
from job_sources import JOB_SOURCES
from sources import SOURCES
from upsert import upsert_programs
from upsert_jobs import upsert_jobs


def start_run(conn) -> int:
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO crawl_runs (started_at, status) VALUES (%s, 'running')",
            (datetime.now(),),
        )
        return int(cur.lastrowid)


def finish_run(
    conn,
    run_id: int,
    status: str,
    new_count: int,
    updated_count: int,
    error_message: str | None = None,
) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE crawl_runs
            SET finished_at = %s, status = %s,
                new_count = %s, updated_count = %s, error_message = %s
            WHERE id = %s
            """,
            (datetime.now(), status, new_count, updated_count, error_message, run_id),
        )


def mark_source_success(conn, source_code: str) -> None:
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE sources SET last_success_at = %s WHERE code = %s",
            (datetime.now(), source_code),
        )


def main() -> None:
    total_new = 0
    total_updated = 0
    errors: list[str] = []

    with get_connection() as conn:
        run_id = start_run(conn)
        conn.commit()

        try:
            for source in SOURCES:
                try:
                    programs = source.collect()
                    new_count, updated_count = upsert_programs(conn, programs)
                    total_new += new_count
                    total_updated += updated_count
                    mark_source_success(conn, source.code)
                    conn.commit()
                    print(
                        f"[{source.code}] collected={len(programs)} "
                        f"new={new_count} updated={updated_count}"
                    )
                except Exception as exc:  # 소스 단위 실패는 전체 중단하지 않음
                    msg = f"{source.code}: {exc}"
                    errors.append(msg)
                    print(f"[error] {msg}")
                    conn.rollback()
                finally:
                    source.close()

            if not JOB_SOURCES:
                print("[jobs] no sources configured — skip")
            for source in JOB_SOURCES:
                try:
                    jobs = source.collect()
                    new_count, updated_count = upsert_jobs(conn, jobs)
                    total_new += new_count
                    total_updated += updated_count
                    mark_source_success(conn, source.code)
                    conn.commit()
                    print(
                        f"[job:{source.code}] collected={len(jobs)} "
                        f"new={new_count} updated={updated_count}"
                    )
                except Exception as exc:
                    msg = f"job:{source.code}: {exc}"
                    errors.append(msg)
                    print(f"[error] {msg}")
                    conn.rollback()
                finally:
                    source.close()

            status = "success" if not errors else "failed"
            finish_run(
                conn,
                run_id,
                status,
                total_new,
                total_updated,
                "; ".join(errors) if errors else None,
            )
            conn.commit()
        except Exception as exc:
            finish_run(conn, run_id, "failed", total_new, total_updated, str(exc))
            conn.commit()
            raise

    print(f"done new={total_new} updated={total_updated} errors={len(errors)}")


if __name__ == "__main__":
    main()
