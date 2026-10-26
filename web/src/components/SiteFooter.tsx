import { getDataAsOf } from "@/lib/programs";

export async function SiteFooter() {
  const dataAsOf = await getDataAsOf();

  return (
    <footer className="border-t border-white/10 bg-[#070b14] px-5 py-10 text-sm text-white/50 sm:px-8">
      <div className="mx-auto flex max-w-6xl flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="font-[family-name:var(--font-display)] text-lg text-white/80">
            돈고래 DonGorae
          </p>
          <p className="mt-1">창업 공고와 개발 일감을 한눈에.</p>
        </div>
        <p>데이터 기준: {dataAsOf} (주 1회 수집)</p>
      </div>
    </footer>
  );
}
