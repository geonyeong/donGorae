import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { workTypeLabel } from "@/lib/jobs";
import type { Job } from "@/lib/types";
import { cn } from "@/lib/utils";

type Props = {
  job: Job;
};

export function JobCard({ job }: Props) {
  const skills = job.skills.slice(0, 3);

  return (
    <Link href={`/jobs/${job.id}`} className="block h-full">
      <Card
        className={cn(
          "h-full gap-2 rounded-none border-white/10 bg-white/[0.03] py-0 transition",
          "hover:border-primary/40 hover:bg-white/[0.06]",
        )}
      >
        <CardHeader className="p-5 pb-0 sm:p-6 sm:pb-0">
          <div className="flex items-start justify-between gap-3">
            <div className="flex flex-wrap gap-2">
              <Badge className="rounded-none bg-primary/15 text-primary hover:bg-primary/15">
                {workTypeLabel(job.workType)}
              </Badge>
              {skills.map((skill) => (
                <Badge
                  key={skill}
                  variant="secondary"
                  className="rounded-none bg-white/5 text-white/60 hover:bg-white/5"
                >
                  {skill}
                </Badge>
              ))}
            </div>
            <span
              className={cn(
                "shrink-0 text-xs font-semibold tracking-wide",
                job.status === "closed" ? "text-white/40" : "text-primary",
              )}
            >
              {job.status === "closed" ? "마감" : "모집중"}
            </span>
          </div>
          <CardTitle className="mt-3 font-[family-name:var(--font-display)] text-lg leading-snug text-white sm:text-xl">
            {job.title}
          </CardTitle>
        </CardHeader>
        <CardContent className="p-5 pt-2 sm:p-6 sm:pt-2">
          {job.summary && (
            <p className="line-clamp-2 text-sm leading-relaxed text-white/55">{job.summary}</p>
          )}
          <p className="mt-4 text-xs text-white/40">
            {[job.budgetText, job.durationText, job.organization ?? job.sourceCode]
              .filter(Boolean)
              .join(" · ")}
          </p>
        </CardContent>
      </Card>
    </Link>
  );
}
