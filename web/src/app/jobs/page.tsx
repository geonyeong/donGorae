import Link from "next/link";
import { JobCard } from "@/components/JobCard";
import { Button, buttonVariants } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  BUDGET_BAND_OPTIONS,
  getJobSourceCodes,
  getJobs,
  JOB_SKILLS,
  WORK_TYPE_OPTIONS,
} from "@/lib/jobs";
import { cn } from "@/lib/utils";

type SearchParams = Promise<{
  q?: string;
  workType?: string;
  skill?: string;
  budget?: string;
  source?: string;
}>;

export const dynamic = "force-dynamic";

export const metadata = {
  title: "개발 일감",
};

export default async function JobsPage({
  searchParams,
}: {
  searchParams: SearchParams;
}) {
  const params = await searchParams;
  const [jobs, sources] = await Promise.all([
    getJobs({
      q: params.q,
      workType: params.workType,
      skill: params.skill,
      budget: params.budget,
      source: params.source,
    }),
    getJobSourceCodes(),
  ]);

  const filters = [
    { label: "전체", href: "/jobs" },
    ...WORK_TYPE_OPTIONS.map((option) => ({
      label: option.label,
      href: `/jobs?workType=${option.value}`,
    })),
    ...BUDGET_BAND_OPTIONS.map((option) => ({
      label: option.label,
      href: `/jobs?budget=${option.value}`,
    })),
    ...JOB_SKILLS.map((skill) => ({
      label: skill,
      href: `/jobs?skill=${encodeURIComponent(skill)}`,
    })),
    ...sources.map((source) => ({
      label: source,
      href: `/jobs?source=${source}`,
    })),
  ];

  return (
    <div className="bg-background px-5 pb-20 pt-28 sm:px-8 sm:pt-32">
      <div className="mx-auto max-w-6xl">
        <h1 className="font-[family-name:var(--font-display)] text-4xl text-white sm:text-5xl">
          개발 일감
        </h1>
        <p className="mt-3 text-muted-foreground">
          프리랜서 개발 모집을 모았습니다. 지원은 원문 사이트에서 진행합니다.
        </p>

        <form className="mt-8 flex flex-col gap-3 sm:flex-row" action="/jobs" method="get">
          <Input
            type="search"
            name="q"
            defaultValue={params.q ?? ""}
            placeholder="키워드 검색 (예: React, 원격)"
            className="h-11 flex-1 rounded-none border-white/15 bg-white/5 text-white placeholder:text-white/35"
          />
          <Button type="submit" className="h-11 rounded-none px-6">
            검색
          </Button>
        </form>

        <div className="mt-6 flex flex-wrap gap-2">
          {filters.map((filter) => (
            <Link
              key={filter.href}
              href={filter.href}
              className={cn(
                buttonVariants({ variant: "outline", size: "sm" }),
                "rounded-none border-white/15 text-white/70 hover:border-primary/40 hover:text-primary",
              )}
            >
              {filter.label}
            </Link>
          ))}
        </div>

        <div className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {jobs.map((job) => (
            <JobCard key={job.id} job={job} />
          ))}
        </div>

        {jobs.length === 0 && (
          <p className="mt-16 text-center text-muted-foreground">
            조건에 맞는 일감이 없습니다. 수집 소스는 확정 후 주 1회 반영됩니다.
          </p>
        )}
      </div>
    </div>
  );
}
