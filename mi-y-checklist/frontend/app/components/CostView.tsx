"use client";

import { useEffect, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:7891";
const SLUG = "mi-y-kontum-research";

type Section = { title: string; tasks: Array<{ id: string; text: string; done: boolean }>; notes?: string[] };
type FileData = { frontmatter: any; sections: Section[] };

export default function CostView() {
  const [data, setData] = useState<FileData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE}/api/projects/${SLUG}/files/cost`)
      .then((r) => r.json())
      .then((d) => { setData(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-6 text-center text-slate-400">Đang tải...</div>;
  if (!data) return <div className="p-6 text-center text-red-400">Lỗi tải dữ liệu</div>;

  return (
    <div className="space-y-4">
      <div className="rounded-2xl bg-red-50 p-4 ring-1 ring-red-200">
        <h1 className="text-xl font-bold text-red-700">📊 Bảng Cost Nguyên Liệu</h1>
        <p className="mt-1 text-sm text-red-600">
          Edit bất kỳ ô <strong>Đơn giá</strong> nào để tính lại tổng cost theo từng công thức.
        </p>
        <button className="mt-3 rounded-lg bg-red-500 px-4 py-2 text-sm font-bold text-white hover:bg-red-600">
          + Thêm nguyên liệu mới
        </button>
      </div>

      {data.sections.map((sec, si) => (
        <div key={si} className="overflow-hidden rounded-2xl bg-white shadow-sm">
          <div className="flex items-center justify-between border-b border-slate-100 bg-red-50/60 px-4 py-2.5">
            <h2 className="text-sm font-bold text-red-700">{sec.title}</h2>
            <span className="text-xs font-medium text-red-500">{sec.tasks.length} dòng</span>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <tbody className="divide-y divide-slate-100">
                {sec.tasks.map((t) => (
                  <tr key={t.id} className="hover:bg-slate-50">
                    <td className="px-4 py-2 align-top text-slate-700">{t.text}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ))}
    </div>
  );
}
