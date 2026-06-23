"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { AlertTriangle, ArrowLeft, BriefcaseBusiness, CheckCircle2, Lightbulb, Puzzle } from "lucide-react";

import { Header } from "@/components/header";
import { Button } from "@/components/ui/button";
import type { ReviewResult } from "@/lib/api";

const sections = [
  { key: "strengths", title: "Điểm mạnh", icon: CheckCircle2, color: "text-green", bg: "bg-mint" },
  { key: "weaknesses", title: "Điểm cần cải thiện", icon: AlertTriangle, color: "text-coral", bg: "bg-orange-50" },
  { key: "missingSkills", title: "Kỹ năng còn thiếu", icon: Puzzle, color: "text-violet-600", bg: "bg-violet-50" },
  { key: "suggestions", title: "Gợi ý hành động", icon: Lightbulb, color: "text-amber-600", bg: "bg-amber-50" },
] as const;

export default function ReviewPage() {
  const [result, setResult] = useState<ReviewResult | null>(null);
  const [ready, setReady] = useState(false);
  useEffect(() => {
    const stored = sessionStorage.getItem("cv-review-result");
    if (stored) { try { setResult(JSON.parse(stored) as ReviewResult); } catch { sessionStorage.removeItem("cv-review-result"); } }
    setReady(true);
  }, []);

  if (!ready) return <main className="min-h-screen bg-cream"><Header /></main>;
  if (!result) return <main className="min-h-screen bg-cream"><Header /><div className="mx-auto max-w-xl px-5 py-24 text-center"><h1 className="font-serif text-4xl font-semibold">Chưa có kết quả phân tích</h1><p className="mt-3 text-ink/60">Hãy tải lên một CV để bắt đầu.</p><Button asChild className="mt-7"><Link href="/">Tải CV lên</Link></Button></div></main>;

  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_85%_5%,#dff4e8_0,transparent_25%)]">
      <Header />
      <div className="mx-auto max-w-6xl px-5 pb-20 pt-8 sm:px-8">
        <Link href="/" className="inline-flex items-center gap-2 text-sm font-bold text-ink/55 hover:text-green"><ArrowLeft size={16} /> Phân tích CV khác</Link>
        <div className="mt-7 grid gap-5 lg:grid-cols-[300px_1fr] animate-fade-in-up">
          <aside className="h-fit rounded-[2rem] bg-ink p-7 text-white lg:sticky lg:top-6 shadow-xl">
            <p className="text-xs font-bold uppercase tracking-[0.18em] text-white/50">Điểm ATS</p>
            <div className="relative mx-auto my-8 grid size-44 place-items-center rounded-full transition-transform duration-500 hover:scale-105" style={{ background: `conic-gradient(#7ed6ad ${result.score * 3.6}deg, rgba(255,255,255,.1) 0)` }}><div className="grid size-36 place-items-center rounded-full bg-ink text-center"><span><strong className="font-serif text-6xl">{result.score}</strong><small className="block text-white/45">trên 100</small></span></div></div>
            <p className="text-center text-sm leading-6 text-white/60">{result.score >= 80 ? "CV có nền tảng tốt. Hãy tinh chỉnh để nổi bật hơn." : result.score >= 60 ? "CV khá ổn nhưng vẫn còn khoảng trống cần cải thiện." : "CV cần được củng cố trước khi ứng tuyển."}</p>
          </aside>
          <div className="space-y-5">
            <div><p className="text-sm font-bold uppercase tracking-[0.14em] text-green">Báo cáo của bạn</p><h1 className="mt-2 font-serif text-4xl font-semibold sm:text-5xl">Phân tích CV chuyên sâu</h1></div>
            <div className="grid gap-5 md:grid-cols-2">
              {sections.map(({ key, title, icon: Icon, color, bg }) => (
                <section key={key} className="rounded-3xl p-6 glass-card interactive-card shadow-sm">
                  <span className={`grid size-11 place-items-center rounded-2xl ${bg} ${color} shadow-inner`}><Icon size={22} /></span>
                  <h2 className="mt-5 font-serif text-2xl font-semibold">{title}</h2>
                  {result[key].length ? (
                    <ul className="mt-4 space-y-3">
                      {result[key].map((item, i) => (
                        <li key={i} className="flex gap-3 text-sm leading-6 text-ink/75">
                          <span className="mt-2 size-1.5 shrink-0 rounded-full bg-green" />
                          {item}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="mt-4 text-sm text-ink/45">Không có nhận xét trong mục này.</p>
                  )}
                </section>
              ))}
            </div>
            <section className="rounded-3xl bg-green p-6 text-white sm:p-8 shadow-lg transition-transform duration-300 hover:scale-[1.01]">
              <span className="flex items-center gap-3">
                <BriefcaseBusiness />
                <h2 className="font-serif text-2xl font-semibold">Vị trí phù hợp</h2>
              </span>
              <div className="mt-5 flex flex-wrap gap-2">
                {result.suitableRoles.map((role) => (
                  <span key={role} className="rounded-full bg-white/15 px-4 py-2 text-sm font-semibold hover:bg-white/25 transition-colors cursor-default">
                    {role}
                  </span>
                ))}
              </div>
            </section>
          </div>
        </div>
      </div>
    </main>
  );
}
