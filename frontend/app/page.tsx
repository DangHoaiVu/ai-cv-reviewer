import { ArrowDown, CheckCircle2, Lightbulb, ScanSearch } from "lucide-react";

import { Header } from "@/components/header";
import { UploadCard } from "@/components/upload-card";

const features = [
  { icon: ScanSearch, title: "Chấm điểm ATS", text: "Biết CV đang thân thiện với hệ thống tuyển dụng đến mức nào." },
  { icon: CheckCircle2, title: "Phân tích rõ ràng", text: "Nhìn ra điểm mạnh, điểm yếu và kỹ năng còn thiếu chỉ trong vài phút." },
  { icon: Lightbulb, title: "Gợi ý thực tế", text: "Nhận các bước cải thiện cụ thể cùng vị trí phù hợp với hồ sơ." },
];

export default function Home() {
  return (
    <main className="min-h-screen overflow-hidden bg-[radial-gradient(circle_at_15%_10%,#dff4e8_0,transparent_28%),radial-gradient(circle_at_90%_35%,#f7d8cf_0,transparent_24%)]">
      <Header />
      <section className="mx-auto grid max-w-6xl items-center gap-12 px-5 pb-24 pt-12 sm:px-8 lg:grid-cols-[1fr_0.9fr] lg:pt-20 animate-fade-in-up">
        <div>
          <span className="inline-flex items-center gap-2 rounded-full bg-mint px-3 py-1.5 text-xs font-bold uppercase tracking-[0.16em] text-green animate-float">AI CV Reviewer <ArrowDown size={13} /></span>
          <h1 className="mt-6 max-w-2xl font-serif text-5xl font-semibold leading-[1.1] tracking-tight sm:text-7xl">CV tốt hơn bắt đầu từ một góc nhìn <span className="italic text-green">rõ hơn.</span></h1>
          <p className="mt-6 max-w-xl text-base leading-7 text-ink/65 sm:text-lg">Tải CV lên để nhận điểm ATS, phân tích chuyên sâu và những gợi ý cải thiện có thể áp dụng ngay.</p>
          <div className="mt-9 flex flex-wrap gap-x-7 gap-y-3 text-sm font-semibold text-ink/60">
            <span>✓ Phân tích bằng Gemini</span><span>✓ Không cần đăng ký</span><span>✓ Phản hồi tiếng Việt</span>
          </div>
        </div>
        <UploadCard />
      </section>
      <section className="border-t border-ink/10 bg-white/70">
        <div className="mx-auto grid max-w-6xl gap-6 px-5 py-16 sm:px-8 md:grid-cols-3">
          {features.map(({ icon: Icon, title, text }, index) => (
            <article key={title} className="rounded-3xl p-6 glass-card interactive-card shadow-sm">
              <span className="mb-8 flex items-center justify-between">
                <span className="p-3 bg-mint rounded-2xl text-green inline-block"><Icon size={22} /></span>
                <small className="font-serif text-xl text-ink/25 font-bold">0{index + 1}</small>
              </span>
              <h2 className="font-serif text-2xl font-semibold">{title}</h2>
              <p className="mt-2 text-sm leading-6 text-ink/55">{text}</p>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}
