import type { Metadata } from "next";

import "./globals.css";

export const metadata: Metadata = {
  title: "CV Insight | AI CV Reviewer",
  description: "Phân tích CV, chấm điểm ATS và nhận gợi ý cải thiện bằng AI.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="vi"><body>{children}</body></html>;
}
