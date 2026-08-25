"use client";

import { useEffect, useState, useCallback, useMemo } from "react";
import ChatWidget from "./components/ChatWidget";
import POS from "./components/POS";
import CostView from "./components/CostView";
import OrdersView from "./components/OrdersView";
import POSFloatingButton from "./components/POSFloatingButton";

type Task = { id: string; text: string; done: boolean };
type Section = { title: string; tasks: Task[]; notes?: string[] };
type File = { frontmatter: Record<string, string>; sections: Section[] };

const PROJECT = "mi-y-kontum-research";
const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:7891";
const API = (path: string) => `${API_BASE}${path}`;

const FILES = [
  { key: "checklist",   label: "Checklist",        icon: "✅", accent: "emerald" },
  { key: "ingredients", label: "Nguyên liệu",      icon: "🛒", accent: "amber"  },
  { key: "recipes",     label: "Công thức",        icon: "🍝", accent: "rose"   },
  { key: "budget",      label: "Ngân sách",        icon: "💰", accent: "violet" },
  { key: "calendar",    label: "TikTok Calendar",  icon: "📅", accent: "sky"    },
  { key: "cost",        label: "Quản lý Cost",     icon: "📊", accent: "red"    },
  { key: "orders",      label: "Đơn hàng",         icon: "📦", accent: "indigo" },
  { key: "sales",       label: "Bán hàng",         icon: "🛒", accent: "green"  },
] as const;

type FileKey = typeof FILES[number]["key"];

const ACCENT: Record<string, { bg: string; ring: string; text: string; chip: string }> = {
  emerald: { bg: "bg-emerald-50",   ring: "ring-emerald-200",   text: "text-emerald-700",   chip: "bg-emerald-500"   },
  amber:   { bg: "bg-amber-50",     ring: "ring-amber-200",     text: "text-amber-700",     chip: "bg-amber-500"     },
  rose:    { bg: "bg-rose-50",      ring: "ring-rose-200",      text: "text-rose-700",      chip: "bg-rose-500"      },
  violet:  { bg: "bg-violet-50",    ring: "ring-violet-200",    text: "text-violet-700",    chip: "bg-violet-500"    },
  sky:     { bg: "bg-sky-50",       ring: "ring-sky-200",       text: "text-sky-700",       chip: "bg-sky-500"       },
  red:     { bg: "bg-red-50",       ring: "ring-red-200",       text: "text-red-700",       chip: "bg-red-500"       },
  indigo:  { bg: "bg-indigo-50",    ring: "ring-indigo-200",    text: "text-indigo-700",    chip: "bg-indigo-500"    },
  green:   { bg: "bg-green-50",     ring: "ring-green-200",     text: "text-green-700",     chip: "bg-green-500"     },
};

/** Safely convert task text + URL to React nodes (no innerHTML, no XSS). */
function linkifyText(text: string): React.ReactNode {
  const re = /(https?:\/\/[^\s)]+)/g;
  const parts = text.split(re);
  return parts.map((part, i) => {
    if (i % 2 === 1) {
      // URL — validate + open in new tab
      try {
        const u = new URL(part);
        if (u.protocol === "http:" || u.protocol === "https:") {
          return (
            <a key={i} href={part} target="_blank" rel="noopener noreferrer"
               className="ml-0.5 text-sky-600 underline hover:text-sky-700">🔗</a>
          );
        }
      } catch {}
      return <span key={i}>{part}</span>;
    }
    return <span key={i}>{part}</span>;
  });
}

export default function Home() {
  const [activeTab, setActiveTab] = useState<FileKey>("checklist");
  const [files, setFiles] = useState<Record<string, File>>({});
  const [err, setErr] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [filter, setFilter] = useState<"all" | "todo" | "done">("all");
  const [search, setSearch] = useState("");
  const [newTask, setNewTask] = useState<{ phase: string; text: string }>({ phase: "", text: "" });

  const loadFile = useCallback(async (key: FileKey) => {
    try {
      const r = await fetch(API(`/api/projects/${PROJECT}/files/${key}`));
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const data = await r.json();
      setFiles((prev) => ({ ...prev, [key]: data }));
      setErr(null);
    } catch (e: any) {
      setErr(`${key}: ${e?.message || "load failed"}`);
    }
  }, []);

  useEffect(() => {
    FILES.forEach((f) => loadFile(f.key as FileKey));
  }, [loadFile]);

  const toggle = async (file: FileKey, taskId: string, done: boolean) => {
    setBusy(true);
    try {
      const r = await fetch(
        API(`/api/projects/${PROJECT}/files/${file}/tasks/${taskId}`),
        { method: "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ done }) }
      );
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      await loadFile(file);
    } catch (e: any) {
      setErr(`${file}: ${e?.message || "toggle failed"}`);
    } finally {
      setBusy(false);
    }
  };

  const addTask = async (file: FileKey) => {
    if (!newTask.phase || !newTask.text.trim()) return;
    setBusy(true);
    try {
      const r = await fetch(API(`/api/projects/${PROJECT}/files/${file}/tasks`), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ phase: newTask.phase, text: newTask.text.trim() }),
      });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      setNewTask({ phase: "", text: "" });
      await loadFile(file);
    } catch (e: any) {
      setErr(`${file}: ${e?.message || "add failed"}`);
    } finally {
      setBusy(false);
    }
  };

  const del = async (file: FileKey, taskId: string) => {
    if (!confirm("Xóa task này?")) return;
    setBusy(true);
    try {
      const r = await fetch(
        API(`/api/projects/${PROJECT}/files/${file}/tasks/${taskId}`),
        { method: "DELETE" }
      );
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      await loadFile(file);
    } catch (e: any) {
      setErr(`${file}: ${e?.message || "delete failed"}`);
    } finally {
      setBusy(false);
    }
  };

  const stats = (data?: File) => {
    if (!data) return { total: 0, done: 0 };
    const total = data.sections.reduce((n, s) => n + s.tasks.length, 0);
    const done  = data.sections.reduce((n, s) => n + s.tasks.filter((t) => t.done).length, 0);
    return { total, done };
  };

  const filteredSections = useMemo(() => {
    const data = files[activeTab];
    if (!data) return [];
    return data.sections
      .map((sec) => ({
        ...sec,
        tasks: sec.tasks.filter((t) => {
          if (filter === "todo" && t.done) return false;
          if (filter === "done" && !t.done) return false;
          if (search && !t.text.toLowerCase().includes(search.toLowerCase())) return false;
          return true;
        }),
      }))
      .filter((sec) => sec.tasks.length > 0);
  }, [files, activeTab, filter, search]);

  const tabStats = (key: FileKey) => stats(files[key]);
  const accent = (key: string) => ACCENT[FILES.find((f) => f.key === key)?.accent || "emerald"];

  return (
    <div className="min-h-screen bg-slate-50">
      {/* HEADER */}
      <header className="sticky top-0 z-30 border-b border-slate-200 bg-white/90 backdrop-blur-md">
        <div className="mx-auto max-w-5xl px-4 py-3">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-orange-500 to-rose-500 text-lg shadow-sm">
              🍝
            </div>
            <div className="flex-1">
              <h1 className="text-lg font-bold text-slate-900 leading-tight">Mì Ý Yum Yum</h1>
              <p className="text-xs text-slate-500">Kon Tum · cloud kitchen launch dashboard</p>
            </div>
            <a
              href="https://miy-yum-yum.vercel.app"
              className="hidden text-xs text-slate-400 md:block"
            >miy-yum-yum.vercel.app</a>
          </div>

          {/* TABS */}
          <nav className="-mb-px mt-3 flex gap-1 overflow-x-auto">
            {FILES.map((f) => {
              const isActive = activeTab === f.key;
              const s = tabStats(f.key as FileKey);
              const a = ACCENT[f.accent];
              return (
                <button
                  key={f.key}
                  onClick={() => { setActiveTab(f.key as FileKey); setFilter("all"); setSearch(""); }}
                  className={`flex items-center gap-1.5 whitespace-nowrap border-b-2 px-3 py-2 text-sm font-medium transition ${
                    isActive
                      ? `border-current ${a.text}`
                      : "border-transparent text-slate-500 hover:text-slate-800"
                  }`}
                >
                  <span>{f.icon}</span>
                  <span>{f.label}</span>
                  {s.total > 0 && (
                    <span className={`rounded-full px-1.5 py-0.5 text-[10px] font-bold ${
                      isActive ? `${a.chip} text-white` : "bg-slate-200 text-slate-600"
                    }`}>
                      {s.done}/{s.total}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>
        </div>
      </header>

      {err && (
        <div className="mx-auto mt-3 max-w-5xl px-4">
          <div className="rounded-lg bg-red-50 px-4 py-2.5 text-sm text-red-700 ring-1 ring-red-200">
            ⚠️ {err}. <span className="text-red-500">Kiểm tra backend (Tailscale Funnel) + Mac còn bật.</span>
          </div>
        </div>
      )}

      <main className="mx-auto max-w-5xl px-3 py-4 sm:px-4 sm:py-5">
        {/* STATS + PROGRESS */}
        {(() => {
          const data = files[activeTab];
          const s = stats(data);
          const pct = s.total ? Math.round((s.done * 100) / s.total) : 0;
          const a = accent(activeTab);
          return (
            <div className={`mb-5 rounded-2xl ${a.bg} p-4 ring-1 ${a.ring}`}>
              <div className="mb-2 flex items-center justify-between">
                <div>
                  <div className="text-sm font-medium text-slate-700">
                    {s.done}/{s.total} task đã hoàn thành
                  </div>
                  <div className="text-xs text-slate-500">
                    {data?.frontmatter.last_modified ? `Cập nhật: ${data.frontmatter.last_modified}` : "Đang tải..."}
                    {data?.frontmatter.title ? ` · ${data.frontmatter.title}` : ""}
                  </div>
                </div>
                <div className={`text-3xl font-bold ${a.text}`}>{pct}%</div>
              </div>
              <div className="h-2 overflow-hidden rounded-full bg-white">
                <div className={`h-full ${a.chip} transition-all duration-500`} style={{ width: `${pct}%` }} />
              </div>
            </div>
          );
        })()}

        {/* FILTER + SEARCH */}
        <div className="mb-4 flex flex-col gap-2 sm:flex-row sm:items-center">
          <div className="flex rounded-lg bg-white p-1 shadow-sm ring-1 ring-slate-200">
            {(["all", "todo", "done"] as const).map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`rounded-md px-3 py-1 text-xs font-medium transition ${
                  filter === f
                    ? "bg-slate-900 text-white"
                    : "text-slate-600 hover:text-slate-900"
                }`}
              >
                {f === "all" ? "Tất cả" : f === "todo" ? "Chưa xong" : "Đã xong"}
              </button>
            ))}
          </div>
          <input
            type="text"
            placeholder="🔍 Tìm task..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="flex-1 rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-sm shadow-sm focus:border-slate-400 focus:outline-none"
          />
        </div>

        {/* SPECIAL VIEWS for sales/cost/orders */}
        {activeTab === "sales" ? (
          <POS />
        ) : activeTab === "cost" ? (
          <CostView />
        ) : activeTab === "orders" ? (
          <OrdersView />
        ) : (
          <>
        {/* TASK LISTS */}
        {filteredSections.length === 0 && (
          <div className="rounded-2xl bg-white p-12 text-center shadow-sm ring-1 ring-slate-200">
            <div className="text-4xl">📋</div>
            <div className="mt-2 text-sm text-slate-500">
              {search ? `Không tìm thấy task nào với "${search}"` : "Chưa có task nào trong tab này"}
            </div>
          </div>
        )}

        <div className="space-y-3">
          {filteredSections.map((sec) => {
            const sectionDone = sec.tasks.filter((t) => t.done).length;
            return (
              <div key={sec.title} className="overflow-hidden rounded-2xl bg-white shadow-sm">
                <div className="flex items-center justify-between border-b border-slate-100 bg-slate-50/60 px-4 py-2.5">
                  <h2 className="text-sm font-bold text-slate-800">{sec.title}</h2>
                  <span className="text-xs font-medium text-slate-500">
                    {sectionDone}/{sec.tasks.length}
                  </span>
                </div>

                <ul className="divide-y divide-slate-100">
                  {sec.tasks.map((t) => (
                    <li key={t.id} className="group flex items-start gap-3 px-4 py-2.5 hover:bg-slate-50/60">
                      <input
                        type="checkbox"
                        className="mt-0.5 h-4 w-4 cursor-pointer flex-shrink-0 rounded border-slate-300 text-emerald-500 focus:ring-emerald-500"
                        checked={t.done}
                        disabled={busy}
                        onChange={(e) => toggle(activeTab, t.id, e.target.checked)}
                      />
                      <span
                        className={`flex-1 text-sm leading-snug break-words ${
                          t.done ? "text-slate-400 line-through" : "text-slate-800"
                        }`}
                      >
                        {linkifyText(t.text)}
                      </span>
                      <button
                        onClick={() => del(activeTab, t.id)}
                        disabled={busy}
                        className="text-slate-300 opacity-0 transition group-hover:opacity-100 hover:text-red-500"
                        title="Xóa"
                      >
                        ✕
                      </button>
                    </li>
                  ))}
                </ul>

                <div className="flex gap-2 border-t border-slate-100 bg-slate-50/40 px-4 py-2.5">
                  <input
                    type="text"
                    placeholder={`+ thêm task vào "${sec.title.slice(0, 30)}${sec.title.length > 30 ? '...' : ''}"`}
                    value={newTask.phase === sec.title ? newTask.text : ""}
                    onFocus={() => setNewTask({ phase: sec.title, text: "" })}
                    onChange={(e) => setNewTask({ phase: sec.title, text: e.target.value })}
                    onKeyDown={(e) => e.key === "Enter" && addTask(activeTab)}
                    className="flex-1 rounded-md border border-slate-200 bg-white px-2.5 py-1.5 text-sm focus:border-slate-400 focus:outline-none"
                  />
                  <button
                    onClick={() => addTask(activeTab)}
                    disabled={busy || newTask.phase !== sec.title || !newTask.text.trim()}
                    className="rounded-md bg-slate-900 px-3 py-1.5 text-sm font-medium text-white disabled:opacity-30"
                  >
                    + Thêm
                  </button>
                </div>
              </div>
            );
          })}
        </div>

          </>
        )}

        <footer className="mt-12 text-center text-xs text-slate-400">
          Built for Tuấn Anh · Hermes Agent · 2026-08-01 · v3.0 redesigned
        </footer>
      </main>

      {/* Floating chat widget — pushes questions into Hermes inbox */}
      <ChatWidget activeTab={activeTab} />
      <POSFloatingButton />
    </div>
  );
}
