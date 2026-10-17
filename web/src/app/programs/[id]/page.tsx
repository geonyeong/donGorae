import Link from "next/link";
import { notFound } from "next/navigation";
import { Badge } from "@/components/ui/badge";
import { buttonVariants } from "@/components/ui/button";
import { getDdayLabel, getProgramById } from "@/lib/programs";
import { cn } from "@/lib/utils";

type Props = {
  params: Promise<{ id: string }>;
};

export async function generateMetadata({ params }: Props) {
  const { id } = await params;
  const program = await getProgramById(Number(id));
  return {
    title: program?.title ?? "공고",
  };
}

export default async function ProgramDetailPage({ params }: Props) {
  const { id } = await params;
  const program = await getProgramById(Number(id));
  if (!program) notFound();

  const dday = getDdayLabel(program.applyEnd, program.status);

  return (
    <article className="bg-background px-5 pb-20 pt-28 sm:px-8 sm:pt-32">
      <div className="mx-auto max-w-3xl">
        <Link
          href="/programs"
          className="text-sm text-white/45 transition hover:text-primary"
        >
          ← 목록으로
        </Link>

        <div className="mt-8 flex flex-wrap items-center gap-2">
          {program.category && (
            <Badge className="rounded-none bg-primary/15 text-primary hover:bg-primary/15">
              {program.category}
            </Badge>
          )}
          <span className="text-sm font-semibold text-primary">{dday}</span>
        </div>

        <h1 className="mt-4 font-[family-name:var(--font-display)] text-3xl leading-tight text-white sm:text-5xl">
          {program.title}
        </h1>

        <dl className="mt-8 grid gap-4 border-y border-white/10 py-6 text-sm sm:grid-cols-2">
          <div>
            <dt className="text-white/40">주관</dt>
            <dd className="mt-1 text-white/85">{program.organization ?? "-"}</dd>
          </div>
          <div>
            <dt className="text-white/40">대상</dt>
            <dd className="mt-1 text-white/85">{program.targetAudience ?? "-"}</dd>
          </div>
          <div>
            <dt className="text-white/40">지역</dt>
            <dd className="mt-1 text-white/85">{program.region ?? "-"}</dd>
          </div>
          <div>
            <dt className="text-white/40">접수 기간</dt>
            <dd className="mt-1 text-white/85">
              {program.applyStart ?? "?"} ~ {program.applyEnd ?? "?"}
            </dd>
          </div>
        </dl>

        {program.summary && (
          <p className="mt-8 text-base leading-relaxed text-white/70">{program.summary}</p>
        )}

        <div className="mt-10">
          <a
            href={program.sourceUrl}
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
          출처: {program.sourceCode} · 수집: {program.collectedAt.slice(0, 10)}
        </p>
      </div>
    </article>
  );
}
