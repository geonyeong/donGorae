import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { Program } from "@/lib/types";
import { getDdayLabel } from "@/lib/programs";
import { cn } from "@/lib/utils";

type Props = {
  program: Program;
  featured?: boolean;
};

export function ProgramCard({ program, featured = false }: Props) {
  const dday = getDdayLabel(program.applyEnd, program.status);

  return (
    <Link href={`/programs/${program.id}`} className="block h-full">
      <Card
        className={cn(
          "h-full rounded-none border-white/10 bg-white/[0.03] transition",
          "hover:border-primary/40 hover:bg-white/[0.06]",
          featured ? "gap-3 py-0" : "gap-2 py-0",
        )}
      >
        <CardHeader className={cn(featured ? "p-7 pb-0 sm:p-9 sm:pb-0" : "p-5 pb-0 sm:p-6 sm:pb-0")}>
          <div className="flex items-start justify-between gap-3">
            <div className="flex flex-wrap gap-2">
              {program.category && (
                <Badge className="rounded-none bg-primary/15 text-primary hover:bg-primary/15">
                  {program.category}
                </Badge>
              )}
              {program.region && (
                <Badge
                  variant="secondary"
                  className="rounded-none bg-white/5 text-white/60 hover:bg-white/5"
                >
                  {program.region}
                </Badge>
              )}
            </div>
            <span
              className={cn(
                "shrink-0 text-xs font-semibold tracking-wide",
                program.status === "closed" ? "text-white/40" : "text-primary",
              )}
            >
              {dday}
            </span>
          </div>
          <CardTitle
            className={cn(
              "font-[family-name:var(--font-display)] leading-snug text-white",
              featured ? "mt-4 text-2xl sm:text-3xl" : "mt-3 text-lg sm:text-xl",
            )}
          >
            {program.title}
          </CardTitle>
        </CardHeader>
        <CardContent className={cn(featured ? "p-7 pt-3 sm:p-9 sm:pt-3" : "p-5 pt-2 sm:p-6 sm:pt-2")}>
          {program.summary && (
            <p className="line-clamp-2 text-sm leading-relaxed text-white/55">
              {program.summary}
            </p>
          )}
          <p className="mt-4 text-xs text-white/40">
            {program.organization ?? "기관 미상"} · {program.sourceCode}
          </p>
        </CardContent>
      </Card>
    </Link>
  );
}
