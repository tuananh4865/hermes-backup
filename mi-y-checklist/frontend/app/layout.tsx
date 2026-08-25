import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Mì Ý Yum Yum — Launch Checklist",
  description: "Quản lý tiến độ mở tiệm mì Ý online tại Kon Tum. Realtime sync về Obsidian.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="vi">
      <body className="min-h-screen antialiased">{children}</body>
    </html>
  );
}
