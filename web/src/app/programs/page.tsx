import Link from "next/link";
import { ProgramCard } from "@/components/ProgramCard";
import { Button, buttonVariants } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { getPrograms } from "@/lib/programs";
import { cn } from "@/lib/utils";

type SearchParams = Promise<{
  q?: string;
  category?: string;
  status?: string;
  region?: string;
}>;

export const metadata = {
  title: "공고 전체",
};

export default async function ProgramsPage({
  searchParams,
}: {
  searchParams: SearchParams;
}) {
  const params = await searchParams;
  const programs = await getPrograms({
    q: params.q,
    category: params.category,
    status: params.status,
    region: params.region,
  });

  const filters = [
    { label: "전체", href: "/programs" },
    { label: "접수중", href: "/programs?status=open" },
    { label: "지원사업", href: "/programs?category=지원사업" },
    { label: "창업", href: "/programs?category=창업" },
    { label: "경진대회", href: "/programs?category=경진대회" },
  ];

  return (
    <div className="bg-background px-5 pb-20 pt-28 sm:px-8 sm:pt-32">
      <div className="mx-auto max-w-6xl">
        <h1 className="font-[family-name:var(--font-display)] text-4xl text-white sm:text-5xl">
          공고 전체
        </h1>
        <p className="mt-3 text-muted-foreground">
          K-Startup · 기업마당 · 창업진흥원 · 중기부 공고를 모았습니다.
        </p>

        <form className="mt-8 flex flex-col gap-3 sm:flex-row" action="/programs" method="get">
          <Input
            type="search"
            name="q"
            defaultValue={params.q ?? ""}
            placeholder="키워드 검색 (예: AI, 예비창업)"
            className="h-11 flex-1 rounded-none border-white/15 bg-white/5 text-white placeholder:text-white/35"
          />
          <Button type="submit" className="h-11 rounded-none px-6">
            검색
          </Button>
        </form>

        <div className="mt-6 flex flex-wrap gap-2">
          {filters.map((f) => (
            <Link
              key={f.href}
              href={f.href}
              className={cn(
                buttonVariants({ variant: "outline", size: "sm" }),
                "rounded-none border-white/15 text-white/70 hover:border-primary/40 hover:text-primary",
              )}
            >
              {f.label}
            </Link>
          ))}
        </div>

        <div className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {programs.map((program) => (
            <ProgramCard key={program.id} program={program} />
          ))}
        </div>

        {programs.length === 0 && (
          <p className="mt-16 text-center text-muted-foreground">
            조건에 맞는 공고가 없습니다.
          </p>
        )}
      </div>
    </div>
  );
}
