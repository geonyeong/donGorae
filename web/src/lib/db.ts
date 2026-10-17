/**
 * MySQL 연결 풀.
 * 로컬에서 DB가 없으면 호출하지 말고 programs.ts의 더미 경로를 사용한다.
 */

import mysql from "mysql2/promise";

let pool: mysql.Pool | null = null;

export function getPool(): mysql.Pool {
  if (!pool) {
    pool = mysql.createPool({
      host: process.env.DATABASE_HOST ?? "127.0.0.1",
      port: Number(process.env.DATABASE_PORT ?? 3306),
      user: process.env.DATABASE_USER ?? "dongorae",
      password: process.env.DATABASE_PASSWORD ?? "dongorae",
      database: process.env.DATABASE_NAME ?? "dongorae",
      waitForConnections: true,
      connectionLimit: 5,
      namedPlaceholders: true,
    });
  }
  return pool;
}
