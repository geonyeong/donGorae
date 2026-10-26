import type { RowDataPacket } from "mysql2";
import { getPool } from "./db";
import type { BudgetBand, Job, JobStatus, WorkType } from "./types";

export const JOB_SKILLS = [
  "React",
  "Java",
  "Python",
  "Node.js",
  "Spring",
  "Android",
  "iOS",
  "Vue",
  "PHP",
  "AWS",
] as const;

export const WORK_TYPE_OPTIONS: { value: WorkType; label: string }[] = [
  { value: "remote", label: "원격" },
  { value: "onsite", label: "상주" },
  { value: "hybrid", label: "혼합" },
];

export const BUDGET_BAND_OPTIONS: { value: Exclude<BudgetBand, "unknown">; label: string }[] = [
  { value: "lt_500", label: "500만 미만" },
  { value: "mid", label: "500만~2천만" },
  { value: "high", label: "2천만 이상" },
];

const WORK_TYPES = new Set<string>(WORK_TYPE_OPTIONS.map((o) => o.value));
const BUDGET_BANDS = new Set<string>(BUDGET_BAND_OPTIONS.map((o) => o.value));
const SKILL_SET = new Set<string>(JOB_SKILLS);

export type JobFilters = {
  q?: string;
  workType?: string;
  skill?: string;
  budget?: string;
  source?: string;
};

type JobRow = RowDataPacket & {
  id: number;
  title: string;
  summary: string | null;
  organization: string | null;
  skills: string | string[] | null;
  work_type: WorkType;
  budget_text: string | null;
  budget_band: BudgetBand;
  duration_text: string | null;
  region: string | null;
  apply_end: Date | string | null;
  status: JobStatus;
  source_code: string;
  source_url: string;
  collected_at: Date | string;
};

const SELECT_COLUMNS = `
  id, title, summary, organization, skills, work_type, budget_text, budget_band,
  duration_text, region, apply_end, status, source_code, source_url, collected_at
`;

function toDateString(value: Date | string | null): string | null {
  if (!value) return null;
  if (typeof value === "string") return value.slice(0, 10);
  return value.toISOString().slice(0, 10);
}

function toIsoString(value: Date | string): string {
  if (typeof value === "string") return value;
  return value.toISOString();
}

function parseSkills(value: JobRow["skills"]): string[] {
  if (!value) return [];
  if (Array.isArray(value)) return value.filter((s) => typeof s === "string");
  try {
    const parsed = JSON.parse(value) as unknown;
    if (!Array.isArray(parsed)) return [];
    return parsed.filter((s): s is string => typeof s === "string");
  } catch {
    return [];
  }
}

function mapRow(row: JobRow): Job {
  const workType = WORK_TYPES.has(row.work_type) ? row.work_type : "remote";
  const budgetBand = (BUDGET_BANDS.has(row.budget_band) || row.budget_band === "unknown"
    ? row.budget_band
    : "unknown") as BudgetBand;

  return {
    id: row.id,
    title: row.title,
    summary: row.summary,
    organization: row.organization,
    skills: parseSkills(row.skills),
    workType,
    budgetText: row.budget_text,
    budgetBand,
    durationText: row.duration_text,
    region: row.region,
    applyEnd: toDateString(row.apply_end),
    status: row.status === "closed" ? "closed" : "open",
    sourceCode: row.source_code,
    sourceUrl: row.source_url,
    collectedAt: toIsoString(row.collected_at),
  };
}

async function queryJobs(sql: string, params: unknown[]): Promise<Job[] | null> {
  try {
    const pool = getPool();
    const [rows] = await pool.query<JobRow[]>(sql, params);
    return rows.map(mapRow);
  } catch (error) {
    console.error("[jobs] DB query failed:", error);
    return null;
  }
}

export function workTypeLabel(workType: WorkType): string {
  return WORK_TYPE_OPTIONS.find((o) => o.value === workType)?.label ?? workType;
}

export async function getJobs(filters: JobFilters = {}): Promise<Job[]> {
  const where: string[] = ["1=1"];
  const params: unknown[] = [];

  if (filters.q) {
    where.push("(title LIKE ? OR summary LIKE ? OR CAST(skills AS CHAR) LIKE ?)");
    const like = `%${filters.q}%`;
    params.push(like, like, like);
  }
  if (filters.workType && WORK_TYPES.has(filters.workType)) {
    where.push("work_type = ?");
    params.push(filters.workType);
  }
  if (filters.skill && SKILL_SET.has(filters.skill)) {
    where.push("JSON_CONTAINS(skills, JSON_QUOTE(?), '$')");
    params.push(filters.skill);
  }
  if (filters.budget && BUDGET_BANDS.has(filters.budget)) {
    where.push("budget_band = ?");
    params.push(filters.budget);
  }
  if (filters.source && /^[a-z0-9_]{1,32}$/.test(filters.source)) {
    where.push("source_code = ?");
    params.push(filters.source);
  }

  const sql = `
    SELECT ${SELECT_COLUMNS}
    FROM jobs
    WHERE ${where.join(" AND ")}
    ORDER BY
      CASE status WHEN 'open' THEN 0 ELSE 1 END,
      apply_end IS NULL, apply_end ASC,
      collected_at DESC,
      id DESC
    LIMIT 200
  `;

  return (await queryJobs(sql, params)) ?? [];
}

export async function getJobById(id: number): Promise<Job | null> {
  const rows = await queryJobs(
    `SELECT ${SELECT_COLUMNS} FROM jobs WHERE id = ? LIMIT 1`,
    [id],
  );
  return rows?.[0] ?? null;
}

export async function getNewestJobs(limit = 3): Promise<Job[]> {
  const rows = await queryJobs(
    `SELECT ${SELECT_COLUMNS}
     FROM jobs
     WHERE status = 'open'
     ORDER BY collected_at DESC, id DESC
     LIMIT ?`,
    [limit],
  );
  return rows ?? [];
}

export async function getJobSourceCodes(): Promise<string[]> {
  try {
    const pool = getPool();
    const [rows] = await pool.query<RowDataPacket[]>(
      "SELECT DISTINCT source_code FROM jobs ORDER BY source_code",
    );
    return rows
      .map((row) => String(row.source_code ?? ""))
      .filter((code) => /^[a-z0-9_]{1,32}$/.test(code));
  } catch {
    return [];
  }
}
