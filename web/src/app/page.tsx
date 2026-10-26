import Link from "next/link";
import { Hero } from "@/components/Hero";
import { JobCard } from "@/components/JobCard";
import { ProgramCard } from "@/components/ProgramCard";
import { getNewestJobs } from "@/lib/jobs";
import { getClosingSoon, getNewest } from "@/lib/programs";

// Docker 빌드 시점에는 DB가 없어 더미가 박제됨 → 요청마다 DB 조회
export const dynamic = "force-dynamic";

export default async function HomePage() {
  const [newest, closing, jobs] = await Promise.all([
    getNewest(2),
    getClosingSoon(6),
    getNewestJobs(3),
  ]);

  return (
    <>
      <Hero />

      <section className="border-t border-white/10 bg-[#0a1220] px-5 py-16 sm:px-8 sm:py-24">
        <div className="mx-auto max-w-6xl">
          <div className="flex items-end justify-between gap-4">
            <div>
              <h2 className="font-[family-name:var(--font-display)] text-3xl text-white sm:text-4xl">
                이번 주 신규
              </h2>
              <p className="mt-2 text-sm text-white/50">최근에 수집된 공고</p>
            </div>
            <Link
              href="/programs"
              className="text-sm text-lime-300 transition hover:text-lime-200"
            >
              더보기
            </Link>
          </div>
          <div className="mt-8 grid gap-4 md:grid-cols-2">
            {newest.map((program) => (
              <ProgramCard key={program.id} program={program} featured />
            ))}
          </div>
        </div>
      </section>

      <section className="border-t border-white/10 px-5 py-16 sm:px-8 sm:py-24">
        <div className="mx-auto max-w-6xl">
          <h2 className="font-[family-name:var(--font-display)] text-3xl text-white sm:text-4xl">
            마감 D-7
          </h2>
          <p className="mt-2 text-sm text-white/50">접수 마감이 가까운 공고</p>
          <div className="mt-8 flex gap-4 overflow-x-auto pb-2">
            {closing.map((program) => (
              <div key={program.id} className="min-w-[280px] max-w-[320px] shrink-0">
                <ProgramCard program={program} />
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="border-t border-white/10 bg-[#0a1220] px-5 py-16 sm:px-8 sm:py-24">
        <div className="mx-auto max-w-6xl">
          <div className="flex items-end justify-between gap-4">
            <div>
              <h2 className="font-[family-name:var(--font-display)] text-3xl text-white sm:text-4xl">
                이번 주 일감
              </h2>
              <p className="mt-2 text-sm text-white/50">프리랜서 개발 모집</p>
            </div>
            <Link
              href="/jobs"
              className="text-sm text-lime-300 transition hover:text-lime-200"
            >
              일감 더보기
            </Link>
          </div>
          {jobs.length > 0 ? (
            <div className="mt-8 grid gap-4 md:grid-cols-3">
              {jobs.map((job) => (
                <JobCard key={job.id} job={job} />
              ))}
            </div>
          ) : (
            <p className="mt-8 text-sm text-white/45">
              아직 수집된 일감이 없습니다. 소스를 확정한 뒤 주 1회 수집합니다.
            </p>
          )}
        </div>
      </section>
    </>
  );
}
