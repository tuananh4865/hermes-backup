"use client";

import { useEffect, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:7891";
const SLUG = "mi-y-kontum-research";

type Section = { title: string; tasks: Array<{ id: string; text: string; done: boolean }>; notes?: string[] };
type FileData = { frontmatter: any; sections: Section[] };

export default function OrdersView() {
  const [data, setData] = useState<FileData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE}/api/projects/${SLUG}/files/orders`)
      .then((r) => r.json())
      .then((d) => { setData(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-6 text-center text-slate-400">Đang tải...</div>;
  if (!data) return <div className="p-6 text-center text-red-400">Lỗi tải dữ liệu</div>;

  return (
    <div className="space-y-4">
      <div className="rounded-2xl bg-indigo-50 p-4 ring-1 ring-indigo-200">
        <h1 className="text-xl font-bold text-indigo-700">📦 Lịch sử Đơn hàng</h1>
        <p className="mt-1 text-sm text-indigo-600">
          Đơn mới tạo qua POS sẽ tự động xuất hiện ở đây. Click vào đơn để xem chi tiết / sửa.
        </p>
      </div>

      {data.sections.map((sec, si) => (
        <div key={si} className="overflow-hidden rounded-2xl bg-white shadow-sm">
          <div className="flex items-center justify-between border-b border-slate-100 bg-indigo-50/60 px-4 py-2.5">
            <h2 className="text-sm font-bold text-indigo-700">{sec.title}</h2>
            <span className="text-xs font-medium text-indigo-500">{sec.tasks.length} mục</span>
          </div>
          <div className="divide-y divide-slate-100">
            {sec.tasks.map((t) => (
              <div key={t.id} className="px-4 py-3 hover:bg-slate-50">
                <div className="text-sm font-medium text-slate-700">{t.text}</div>
              </div>
            ))}
            {sec.notes?.map((n, ni) => (
              <div key={`note-${ni}`} className="px-4 py-3 text-xs text-slate-500" dangerouslySetInnerHTML={{ __html: n }} />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
