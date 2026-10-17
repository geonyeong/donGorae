"""MySQL 연결 헬퍼."""

from contextlib import contextmanager
from typing import Generator

import pymysql
from pymysql.connections import Connection

from config import DATABASE


@contextmanager
def get_connection() -> Generator[Connection, None, None]:
    conn = pymysql.connect(
        host=DATABASE["host"],
        port=DATABASE["port"],
        user=DATABASE["user"],
        password=DATABASE["password"],
        database=DATABASE["database"],
        charset=DATABASE["charset"],
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
