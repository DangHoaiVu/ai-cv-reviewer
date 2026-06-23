import type { Metadata } from "next";
import { Manrope, Lora } from "next/font/google";

import "./globals.css";

const manrope = Manrope({
  subsets: ["vietnamese", "latin"],
  variable: "--font-manrope",
  display: "swap",
});

const lora = Lora({
  subsets: ["vietnamese", "latin"],
  variable: "--font-lora",
  display: "swap",
});

export const metadata: Metadata = {
  title: "CV Insight | AI CV Reviewer",
  description: "Phân tích CV, chấm điểm ATS và nhận gợi ý cải thiện bằng AI.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="vi" className={`${manrope.variable} ${lora.variable}`}>
      <body className="font-sans antialiased">{children}</body>
    </html>
  );
}
