"use client";

import { ChangeEvent, DragEvent, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { FileText, LoaderCircle, UploadCloud, X } from "lucide-react";

import { Button } from "@/components/ui/button";
import { uploadAndReview } from "@/lib/api";
import { cn } from "@/lib/utils";

const MAX_SIZE = 10 * 1024 * 1024;

export function UploadCard() {
  const inputRef = useRef<HTMLInputElement>(null);
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [dragging, setDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function selectFile(next: File | undefined) {
    setError("");
    if (!next) return;
    if (next.type !== "application/pdf" && !next.name.toLowerCase().endsWith(".pdf")) {
      setError("Vui lòng chọn đúng tệp PDF.");
      return;
    }
    if (next.size > MAX_SIZE) {
      setError("Tệp PDF không được vượt quá 10 MB.");
      return;
    }
    setFile(next);
  }

  function handleDrop(event: DragEvent<HTMLDivElement>) {
    event.preventDefault();
    setDragging(false);
    selectFile(event.dataTransfer.files[0]);
  }

  async function handleReview() {
    if (!file) return;
    setLoading(true);
    setError("");
    try {
      const result = await uploadAndReview(file);
      sessionStorage.setItem("cv-review-result", JSON.stringify(result));
      router.push("/review");
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Không thể phân tích CV.");
      setLoading(false);
    }
  }

  return (
    <div className="rounded-[2rem] border border-white bg-white/90 p-4 shadow-soft sm:p-6">
      <div
        onDragOver={(event) => { event.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        className={cn("rounded-3xl border-2 border-dashed px-5 py-10 text-center transition sm:py-14", dragging ? "border-green bg-mint/60" : "border-ink/15 bg-cream/60")}
      >
        <input ref={inputRef} type="file" accept="application/pdf,.pdf" className="sr-only" onChange={(e: ChangeEvent<HTMLInputElement>) => selectFile(e.target.files?.[0])} />
        {file ? (
          <div className="mx-auto flex max-w-md items-center gap-4 rounded-2xl border border-ink/10 bg-white p-4 text-left">
            <span className="grid size-12 shrink-0 place-items-center rounded-xl bg-mint text-green"><FileText /></span>
            <div className="min-w-0 flex-1"><p className="truncate font-bold">{file.name}</p><p className="text-sm text-ink/50">{(file.size / 1024 / 1024).toFixed(2)} MB</p></div>
            <button aria-label="Bỏ chọn tệp" onClick={() => setFile(null)} className="rounded-full p-2 text-ink/40 hover:bg-cream hover:text-coral"><X size={18} /></button>
          </div>
        ) : (
          <>
            <span className="mx-auto mb-4 grid size-14 place-items-center rounded-2xl bg-mint text-green"><UploadCloud size={27} /></span>
            <p className="font-bold text-ink">Kéo và thả CV vào đây</p>
            <p className="mt-1 text-sm text-ink/50">PDF, tối đa 10 MB</p>
            <Button variant="outline" className="mt-5" onClick={() => inputRef.current?.click()}>Chọn tệp PDF</Button>
          </>
        )}
      </div>
      {error && <p role="alert" className="mt-4 rounded-xl bg-red-50 px-4 py-3 text-sm font-medium text-red-700">{error}</p>}
      <Button className="mt-4 w-full py-4" disabled={!file || loading} onClick={handleReview}>
        {loading ? <><LoaderCircle className="animate-spin" size={18} /> AI đang phân tích CV...</> : "Phân tích CV miễn phí"}
      </Button>
      <p className="mt-3 text-center text-xs text-ink/40">CV của bạn chỉ được lưu tạm thời để xử lý.</p>
    </div>
  );
}
