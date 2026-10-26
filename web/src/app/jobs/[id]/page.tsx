import Link from "next/link";
import { notFound } from "next/navigation";
import { Badge } from "@/components/ui/badge";
import { buttonVariants } from "@/components/ui/button";
import { getJobById, jobSourceLabel, workTypeLabel } from "@/lib/jobs";
import { cn } from "@/lib/utils";

type Props = {
  params: Promise<{ id: string }>;
};

export const dynamic = "force-dynamic";

export async function generateMetadata({ params }: Props) {
  const { id } = await params;
  const job = await getJobById(Number(id));
  return {
    title: job?.title ?? "일감",
  };
}

export default async function JobDetailPage({ params }: Props) {
  const { id } = await params;
  const job = await getJobById(Number(id));
  if (!job) notFound();

  return (
    <article className="bg-background px-5 pb-20 pt-28 sm:px-8 sm:pt-32">
      <div className="mx-auto max-w-3xl">
        <Link href="/jobs" className="text-sm text-white/45 transition hover:text-primary">
          ← 일감 목록
        </Link>

        <div className="mt-8 flex flex-wrap items-center gap-2">
          <Badge className="rounded-none bg-primary/15 text-primary hover:bg-primary/15">
            {workTypeLabel(job.workType)}
          </Badge>
          {job.skills.map((skill) => (
            <Badge
              key={skill}
              variant="secondary"
              className="rounded-none bg-white/5 text-white/70 hover:bg-white/5"
            >
              {skill}
            </Badge>
          ))}
          <span className="text-sm font-semibold text-primary">
            {job.status === "closed" ? "마감" : "모집중"}
          </span>
        </div>

        <h1 className="mt-4 font-[family-name:var(--font-display)] text-3xl leading-tight text-white sm:text-5xl">
          {job.title}
        </h1>

        <dl className="mt-8 grid gap-4 border-y border-white/10 py-6 text-sm sm:grid-cols-2">
          <div>
            <dt className="text-white/40">발주</dt>
            <dd className="mt-1 text-white/85">{job.organization ?? "-"}</dd>
          </div>
          <div>
            <dt className="text-white/40">예산</dt>
            <dd className="mt-1 text-white/85">{job.budgetText ?? "-"}</dd>
          </div>
          <div>
            <dt className="text-white/40">기간</dt>
            <dd className="mt-1 text-white/85">{job.durationText ?? "-"}</dd>
          </div>
          <div>
            <dt className="text-white/40">지역</dt>
            <dd className="mt-1 text-white/85">{job.region ?? "-"}</dd>
          </div>
          <div>
            <dt className="text-white/40">마감</dt>
            <dd className="mt-1 text-white/85">{job.applyEnd ?? "상시"}</dd>
          </div>
        </dl>

        {job.summary && (
          <p className="mt-8 text-base leading-relaxed text-white/70">{job.summary}</p>
        )}

        <div className="mt-10">
          <a
            href={job.sourceUrl}
            target="_blank"
            rel="noopener noreferrer"
            className={cn(
              buttonVariants({ size: "lg" }),
              "rounded-none bg-primary px-6 text-primary-foreground hover:bg-lime-200",
            )}
          >
            원문 보기
          </a>
        </div>

        <p className="mt-8 text-xs text-white/35">
          출처: {jobSourceLabel(job.sourceCode)} · 수집: {job.collectedAt.slice(0, 10)}
        </p>
      </div>
    </article>
  );
}
