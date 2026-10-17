import type { RowDataPacket } from "mysql2";
import { DATA_AS_OF, DUMMY_PROGRAMS } from "./dummy-programs";
import { getPool } from "./db";
import type { Program, ProgramStatus } from "./types";

export type ProgramFilters = {
  q?: string;
  category?: string;
  status?: string;
  region?: string;
};

type ProgramRow = RowDataPacket & {
  id: number;
  title: string;
  summary: string | null;
  organization: string | null;
  category: string | null;
  region: string | null;
  target_audience: string | null;
  apply_start: Date | string | null;
  apply_end: Date | string | null;
  status: ProgramStatus;
  source_code: string;
  source_url: string;
  collected_at: Date | string;
};

function toDateString(value: Date | string | null): string | null {
  if (!value) return null;
  if (typeof value === "string") return value.slice(0, 10);
  return value.toISOString().slice(0, 10);
}

function toIsoString(value: Date | string): string {
  if (typeof value === "string") return value;
  return value.toISOString();
}

function mapRow(row: ProgramRow): Program {
  return {
    id: row.id,
    title: row.title,
    summary: row.summary,
    organization: row.organization,
    category: row.category,
    region: row.region,
    targetAudience: row.target_audience,
    applyStart: toDateString(row.apply_start),
    applyEnd: toDateString(row.apply_end),
    status: row.status,
    sourceCode: row.source_code,
    sourceUrl: row.source_url,
    collectedAt: toIsoString(row.collected_at),
  };
}

/** 데이터 기준일 기준 D-day (prerender 시 Date.now 사용 금지) */
function daysUntil(end: string | null, asOf: string = DATA_AS_OF): number | null {
  if (!end) return null;
  const endDate = new Date(`${end}T23:59:59+09:00`);
  const asOfDate = new Date(`${asOf}T12:00:00+09:00`);
  return Math.ceil(
    (endDate.getTime() - asOfDate.getTime()) / (1000 * 60 * 60 * 24),
  );
}

export function getDdayLabel(applyEnd: string | null, status: string): string {
  if (status === "closed") return "마감";
  const d = daysUntil(applyEnd);
  if (d === null) return "상시";
  if (d < 0) return "마감";
  if (d === 0) return "D-Day";
  return `D-${d}`;
}

async function queryPrograms(sql: string, params: unknown[] = []): Promise<Program[] | null> {
  try {
    const pool = getPool();
    const [rows] = await pool.query<ProgramRow[]>(sql, params);
    return rows.map(mapRow);
  } catch (error) {
    console.error("[programs] DB query failed, fallback to dummy:", error);
    return null;
  }
}

function filterDummy(filters: ProgramFilters): Program[] {
  let list = [...DUMMY_PROGRAMS];
  if (filters.q) {
    const q = filters.q.toLowerCase();
    list = list.filter(
      (p) =>
        p.title.toLowerCase().includes(q) ||
        (p.summary ?? "").toLowerCase().includes(q) ||
        (p.organization ?? "").toLowerCase().includes(q),
    );
  }
  if (filters.category) list = list.filter((p) => p.category === filters.category);
  if (filters.status) list = list.filter((p) => p.status === filters.status);
  if (filters.region) list = list.filter((p) => p.region === filters.region);
  return list;
}

export async function getPrograms(filters: ProgramFilters = {}): Promise<Program[]> {
  const where: string[] = ["1=1"];
  const params: unknown[] = [];

  if (filters.q) {
    where.push("(title LIKE ? OR summary LIKE ? OR organization LIKE ?)");
    const like = `%${filters.q}%`;
    params.push(like, like, like);
  }
  if (filters.category) {
    where.push("category = ?");
    params.push(filters.category);
  }
  if (filters.status) {
    where.push("status = ?");
    params.push(filters.status);
  }
  if (filters.region) {
    where.push("region = ?");
    params.push(filters.region);
  }

  const sql = `
    SELECT id, title, summary, organization, category, region, target_audience,
           apply_start, apply_end, status, source_code, source_url, collected_at
    FROM programs
    WHERE ${where.join(" AND ")}
    ORDER BY
      CASE status WHEN 'open' THEN 0 WHEN 'upcoming' THEN 1 ELSE 2 END,
      apply_end IS NULL, apply_end ASC, id DESC
    LIMIT 200
  `;

  const rows = await queryPrograms(sql, params);
  // 운영에서는 더미 폴백 금지 (빌드 시 박제 방지). 로컬만 USE_DUMMY_DATA=1
  if (rows) return rows;
  return useDummyFallback() ? filterDummy(filters) : [];
}

function useDummyFallback(): boolean {
  return process.env.USE_DUMMY_DATA === "1" || process.env.NODE_ENV === "development";
}

export async function getProgramById(id: number): Promise<Program | null> {
  const rows = await queryPrograms(
    `SELECT id, title, summary, organization, category, region, target_audience,
            apply_start, apply_end, status, source_code, source_url, collected_at
     FROM programs WHERE id = ? LIMIT 1`,
    [id],
  );
  if (rows) return rows[0] ?? null;
  if (!useDummyFallback()) return null;
  return DUMMY_PROGRAMS.find((p) => p.id === id) ?? null;
}

export async function getClosingSoon(limit = 6): Promise<Program[]> {
  const rows = await queryPrograms(
    `SELECT id, title, summary, organization, category, region, target_audience,
            apply_start, apply_end, status, source_code, source_url, collected_at
     FROM programs
     WHERE status = 'open' AND apply_end IS NOT NULL AND apply_end >= CURDATE()
     ORDER BY apply_end ASC
     LIMIT ?`,
    [limit],
  );
  if (rows) return rows;
  if (!useDummyFallback()) return [];
  return DUMMY_PROGRAMS.filter((p) => p.status === "open" && p.applyEnd)
    .sort((a, b) => (a.applyEnd! > b.applyEnd! ? 1 : -1))
    .slice(0, limit);
}

export async function getNewest(limit = 4): Promise<Program[]> {
  const rows = await queryPrograms(
    `SELECT id, title, summary, organization, category, region, target_audience,
            apply_start, apply_end, status, source_code, source_url, collected_at
     FROM programs
     ORDER BY collected_at DESC, id DESC
     LIMIT ?`,
    [limit],
  );
  if (rows) return rows;
  if (!useDummyFallback()) return [];
  return [...DUMMY_PROGRAMS]
    .sort((a, b) => (a.collectedAt < b.collectedAt ? 1 : -1))
    .slice(0, limit);
}

export async function getDataAsOf(): Promise<string> {
  try {
    const pool = getPool();
    const [rows] = await pool.query<RowDataPacket[]>(
      `SELECT DATE_FORMAT(MAX(collected_at), '%Y-%m-%d') AS d FROM programs`,
    );
    const d = rows[0]?.d as string | null;
    if (d) return d;
  } catch {
    // fallback
  }
  return DATA_AS_OF;
}
