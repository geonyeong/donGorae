import Image from "next/image";
import Link from "next/link";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export function Hero() {
  return (
    <section className="relative isolate min-h-[100svh] overflow-hidden">
      <Image
        src="/brand/hero-whale.jpg"
        alt="돈다발을 뿜는 고래 — 돈고래 브랜드 비주얼"
        fill
        priority
        className="object-cover object-[center_30%]"
        sizes="100vw"
      />
      <div className="absolute inset-0 bg-gradient-to-t from-[#071018] via-[#071018]/70 to-[#071018]/35" />
      <div className="absolute inset-0 bg-gradient-to-r from-[#071018]/80 via-transparent to-transparent" />

      <div className="relative mx-auto flex min-h-[100svh] max-w-6xl flex-col justify-end px-5 pb-16 pt-28 sm:px-8 sm:pb-24 sm:pt-32">
        <p className="animate-fade-up text-sm tracking-[0.2em] text-primary uppercase">
          Startup intel for Korea
        </p>
        <h1 className="animate-fade-up-delay mt-4 font-[family-name:var(--font-display)] text-5xl leading-[1.05] tracking-tight text-white sm:text-7xl lg:text-8xl">
          돈고래
          <span className="mt-2 block text-3xl text-white/75 sm:text-4xl lg:text-5xl">
            DonGorae
          </span>
        </h1>
        <p className="animate-fade-up-delay-2 mt-6 max-w-xl text-base leading-relaxed text-white/75 sm:text-lg">
          창업 경진대회·지원사업을 한곳에. 놓치기 쉬운 마감, 먼저 잡으세요.
        </p>
        <div className="animate-fade-up-delay-2 mt-10 flex flex-wrap gap-3">
          <Link
            href="/programs?status=open"
            className={cn(
              buttonVariants({ size: "lg" }),
              "rounded-none bg-primary px-6 text-primary-foreground hover:bg-lime-200",
            )}
          >
            마감 임박 보기
          </Link>
          <Link
            href="/programs"
            className={cn(
              buttonVariants({ variant: "outline", size: "lg" }),
              "rounded-none border-white/30 bg-transparent text-white hover:border-primary/50 hover:bg-white/5 hover:text-primary",
            )}
          >
            전체 공고
          </Link>
        </div>
      </div>
    </section>
  );
}
