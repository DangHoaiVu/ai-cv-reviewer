import Link from "next/link";
import { FileCheck2 } from "lucide-react";

export function Header() {
  return (
    <header className="mx-auto flex w-full max-w-6xl items-center justify-between px-5 py-6 sm:px-8">
      <Link href="/" className="flex items-center gap-2 font-bold tracking-tight text-ink">
        <span className="grid size-9 place-items-center rounded-xl bg-ink text-white"><FileCheck2 size={19} /></span>
        CV Insight
      </Link>
      <span className="rounded-full border border-ink/10 bg-white/70 px-3 py-1.5 text-xs font-semibold text-ink/60">Powered by Gemini</span>
    </header>
  );
}
