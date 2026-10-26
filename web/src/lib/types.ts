export type ProgramStatus = "upcoming" | "open" | "closed";

export type Program = {
  id: number;
  title: string;
  summary: string | null;
  organization: string | null;
  category: string | null;
  region: string | null;
  targetAudience: string | null;
  applyStart: string | null;
  applyEnd: string | null;
  status: ProgramStatus;
  sourceCode: string;
  sourceUrl: string;
  collectedAt: string;
};

export type WorkType = "remote" | "onsite" | "hybrid";
export type BudgetBand = "lt_500" | "mid" | "high" | "unknown";
export type JobStatus = "open" | "closed";

export type Job = {
  id: number;
  title: string;
  summary: string | null;
  organization: string | null;
  skills: string[];
  workType: WorkType;
  budgetText: string | null;
  budgetBand: BudgetBand;
  durationText: string | null;
  region: string | null;
  applyEnd: string | null;
  status: JobStatus;
  sourceCode: string;
  sourceUrl: string;
  collectedAt: string;
};

export type ApiResponse<T> = {
  success: boolean;
  data: T | null;
  error: string | null;
};
