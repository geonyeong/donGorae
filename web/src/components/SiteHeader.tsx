import Image from "next/image";
import Link from "next/link";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export function SiteHeader() {
  return (
    <header className="absolute inset-x-0 top-0 z-20">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-5 sm:h-20 sm:px-8">
        <Link href="/" className="flex items-center gap-3">
          <Image
            src="/brand/logo.jpg"
            alt="돈고래 로고"
            width={40}
            height={40}
            className="size-9 rounded-md object-cover sm:size-10"
            priority
          />
          <span className="font-[family-name:var(--font-display)] text-xl tracking-tight text-white sm:text-2xl">
            돈고래
            <span className="ml-2 text-sm font-normal text-primary">DonGorae</span>
          </span>
        </Link>
        <nav className="flex items-center gap-1">
          <Link
            href="/programs"
            className={cn(
              buttonVariants({ variant: "ghost" }),
              "text-white/80 hover:bg-white/10 hover:text-primary",
            )}
          >
            공고
          </Link>
          <Link
            href="/jobs"
            className={cn(
              buttonVariants({ variant: "ghost" }),
              "text-white/80 hover:bg-white/10 hover:text-primary",
            )}
          >
            일감
          </Link>
        </nav>
      </div>
    </header>
  );
}
