"use client";

/**
 * Floating chat widget for the Mì Ý Yum Yum dashboard.
 * Sends questions to Hermes Agent inbox (queries-log.md).
 *
 * Features:
 * - Floating action button (bottom-right)
 * - Modal panel with question form + recent history
 * - Auto-fill tab context from current page tab
 * - Polls every 30s for new answers → toast notification
 * - Vietnamese UI
 */

import { useEffect, useRef, useState, useCallback } from "react";

type Query = {
  id: string;
  created_at: string;
  tab: string | null;
  question: string;
  answer: string | null;
  status: "pending" | "answered";
};

type Props = {
  activeTab?: string;
  apiBase?: string;
  project?: string;
};

const POLL_INTERVAL_MS = 30_000;

export default function ChatWidget({
  activeTab = "checklist",
  apiBase,
  project = "mi-y-kontum-research",
}: Props) {
  const base =
    apiBase ||
    process.env.NEXT_PUBLIC_API_BASE ||
    "http://127.0.0.1:7891";
  const url = (p: string) => `${base}${p}`;

  // ---------- State ----------
  const [open, setOpen] = useState(false);
  const [question, setQuestion] = useState("");
  const [tab, setTab] = useState(activeTab);
  const [queries, setQueries] = useState<Query[]>([]);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const [toast, setToast] = useState<string | null>(null);
  const [seenAnsweredIds, setSeenAnsweredIds] = useState<Set<string>>(new Set());
  const [firstLoad, setFirstLoad] = useState(true);
  const listRef = useRef<HTMLDivElement | null>(null);
  const inputRef = useRef<HTMLTextAreaElement | null>(null);

  // ---------- Sync tab prop → state ----------
  useEffect(() => {
    setTab(activeTab);
  }, [activeTab]);

  // ---------- Load list ----------
  const loadQueries = useCallback(
    async (silent = false): Promise<Query[]> => {
      try {
        const r = await fetch(url(`/api/projects/${project}/queries?limit=20`), {
          cache: "no-store",
        });
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        const data = (await r.json()) as { queries: Query[] };
        const list = data.queries || [];
        // Detect newly answered items since last poll
        if (!firstLoad) {
          const newAnswers = list.filter(
            (q) => q.status === "answered" && !seenAnsweredIds.has(q.id)
          );
          if (newAnswers.length > 0) {
            setToast(
              newAnswers.length === 1
                ? `💬 Hermes đã trả lời: "${newAnswers[0].question.slice(0, 40)}${newAnswers[0].question.length > 40 ? "..." : ""}"`
                : `💬 Có ${newAnswers.length} câu trả lời mới từ Hermes`
            );
            // Auto-clear toast after 6 seconds
            setTimeout(() => setToast(null), 6000);
          }
        }
        setSeenAnsweredIds(
          new Set(list.filter((q) => q.status === "answered").map((q) => q.id))
        );
        if (!silent) setErr(null);
        return list;
      } catch (e: any) {
        if (!silent) setErr(`Không kết nối được backend: ${e?.message || e}`);
        return [];
      } finally {
        if (firstLoad) setFirstLoad(false);
      }
    },
    [base, project, seenAnsweredIds, firstLoad]
  );

  // Initial load + open
  useEffect(() => {
    if (!open) return;
    loadQueries(true).then((list) => setQueries(list));
    // Focus input on open
    setTimeout(() => inputRef.current?.focus(), 50);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open]);

  // Polling — every 30s, only when open
  useEffect(() => {
    if (!open) return;
    const id = window.setInterval(() => {
      loadQueries(true).then((list) => {
        if (list.length > 0) setQueries(list);
      });
    }, POLL_INTERVAL_MS);
    return () => window.clearInterval(id);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open]);

  // ---------- Submit ----------
  const submit = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    const q = question.trim();
    if (!q || busy) return;
    setBusy(true);
    setErr(null);
    try {
      const r = await fetch(url(`/api/projects/${project}/queries`), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q, context_tab: tab }),
      });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const data = (await r.json()) as { id: string };
      setQuestion("");
      // Refresh list to show the new pending entry
      const list = await loadQueries(true);
      if (list.length > 0) setQueries(list);
      // Scroll to top of list
      setTimeout(() => {
        if (listRef.current) listRef.current.scrollTop = 0;
      }, 50);
      // Tiny inline confirmation
      setToast(`✅ Đã gửi: ${data.id}`);
      setTimeout(() => setToast(null), 3500);
    } catch (e: any) {
      setErr(`Gửi thất bại: ${e?.message || e}`);
    } finally {
      setBusy(false);
    }
  };

  // ---------- Keyboard: Esc to close, Cmd/Ctrl+K to open ----------
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape" && open) setOpen(false);
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setOpen((o) => !o);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open]);

  // ---------- Counts for badge ----------
  const pendingCount = queries.filter((q) => q.status === "pending").length;
  const answeredCount = queries.filter((q) => q.status === "answered").length;

  // ---------- Render ----------
  return (
    <>
      {/* Floating button */}
      <button
        onClick={() => setOpen((o) => !o)}
        aria-label="Mở chat với Hermes"
        title="Hỏi Hermes (⌘K)"
        className="fixed bottom-5 right-5 z-50 flex h-14 w-14 items-center justify-center rounded-full bg-gradient-to-br from-orange-500 to-rose-500 text-2xl text-white shadow-lg shadow-rose-500/30 ring-1 ring-rose-400 transition hover:scale-105 hover:shadow-xl active:scale-95"
      >
        {open ? "✕" : "💬"}
        {!open && pendingCount > 0 && (
          <span className="absolute -top-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full bg-amber-400 text-[10px] font-bold text-amber-900 ring-2 ring-white">
            {pendingCount}
          </span>
        )}
      </button>

      {/* Toast */}
      {toast && (
        <div className="fixed bottom-24 right-5 z-50 max-w-xs rounded-xl bg-slate-900 px-4 py-2.5 text-sm font-medium text-white shadow-xl ring-1 ring-slate-700 animate-pulse">
          {toast}
        </div>
      )}

      {/* Panel */}
      {open && (
        <div className="fixed bottom-24 right-5 z-50 flex h-[640px] max-h-[80vh] w-[400px] max-w-[calc(100vw-2.5rem)] flex-col overflow-hidden rounded-2xl bg-white shadow-2xl ring-1 ring-slate-200">
          {/* Header */}
          <div className="flex items-center justify-between border-b border-slate-200 bg-gradient-to-r from-orange-500 to-rose-500 px-4 py-3 text-white">
            <div className="flex items-center gap-2">
              <span className="text-lg">💬</span>
              <div>
                <div className="text-sm font-bold leading-tight">Hỏi Hermes</div>
                <div className="text-[10px] opacity-90">
                  {queries.length} câu hỏi · {answeredCount} đã trả lời
                  {pendingCount > 0 && ` · ${pendingCount} chờ`}
                </div>
              </div>
            </div>
            <button
              onClick={() => setOpen(false)}
              className="rounded-md p-1 text-white/80 transition hover:bg-white/20 hover:text-white"
              aria-label="Đóng"
            >
              <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Compose */}
          <form onSubmit={submit} className="border-b border-slate-100 bg-slate-50/60 p-3">
            <div className="mb-2 flex items-center gap-2">
              <label className="text-xs font-medium text-slate-600">Tab:</label>
              <select
                value={tab}
                onChange={(e) => setTab(e.target.value)}
                className="flex-1 rounded-md border border-slate-200 bg-white px-2 py-1 text-xs focus:border-slate-400 focus:outline-none"
              >
                <option value="checklist">✅ Checklist</option>
                <option value="ingredients">🛒 Nguyên liệu</option>
                <option value="recipes">🍝 Công thức</option>
                <option value="budget">💰 Ngân sách</option>
                <option value="calendar">📅 Calendar</option>
                <option value="">— không gắn tab —</option>
              </select>
            </div>
            <textarea
              ref={inputRef}
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
                  e.preventDefault();
                  submit();
                }
              }}
              placeholder="Hỏi Hermes bất cứ điều gì… (⌘+Enter để gửi)"
              rows={3}
              className="w-full resize-none rounded-md border border-slate-200 bg-white px-2.5 py-2 text-sm focus:border-slate-400 focus:outline-none"
            />
            {err && (
              <div className="mt-2 rounded-md bg-red-50 px-2 py-1 text-xs text-red-700 ring-1 ring-red-200">
                ⚠️ {err}
              </div>
            )}
            <div className="mt-2 flex items-center justify-between">
              <span className="text-[10px] text-slate-400">⌘+Enter gửi · Esc đóng</span>
              <button
                type="submit"
                disabled={busy || !question.trim()}
                className="rounded-md bg-slate-900 px-3 py-1.5 text-xs font-bold text-white transition hover:bg-slate-800 disabled:opacity-30"
              >
                {busy ? "Đang gửi…" : "Gửi →"}
              </button>
            </div>
          </form>

          {/* History */}
          <div ref={listRef} className="flex-1 overflow-y-auto bg-slate-50/40">
            {queries.length === 0 ? (
              <div className="flex h-full flex-col items-center justify-center px-6 text-center">
                <div className="text-3xl">💭</div>
                <div className="mt-2 text-sm font-medium text-slate-700">Chưa có câu hỏi nào</div>
                <div className="mt-1 text-xs text-slate-500">
                  Gửi câu hỏi đầu tiên để bắt đầu hội thoại với Hermes.
                </div>
              </div>
            ) : (
              <div className="space-y-2 p-3">
                {queries.map((q) => (
                  <QueryCard key={q.id} q={q} />
                ))}
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="border-t border-slate-100 bg-slate-50 px-4 py-2 text-center text-[10px] text-slate-400">
            Polling mỗi 30s · Câu trả lời sẽ tự xuất hiện khi Hermes reply
          </div>
        </div>
      )}
    </>
  );
}

function QueryCard({ q }: { q: Query }) {
  const isAnswered = q.status === "answered";
  return (
    <div
      className={`overflow-hidden rounded-xl bg-white shadow-sm ring-1 transition ${
        isAnswered ? "ring-emerald-200" : "ring-amber-200"
      }`}
    >
      <div className="flex items-center justify-between border-b border-slate-100 bg-slate-50/60 px-3 py-1.5">
        <div className="flex items-center gap-1.5">
          {isAnswered ? (
            <span className="flex items-center gap-1 rounded-full bg-emerald-100 px-1.5 py-0.5 text-[10px] font-bold text-emerald-700">
              ✓ Trả lời
            </span>
          ) : (
            <span className="flex items-center gap-1 rounded-full bg-amber-100 px-1.5 py-0.5 text-[10px] font-bold text-amber-700">
              ⏳ Chờ
            </span>
          )}
          {q.tab && (
            <span className="rounded-full bg-slate-100 px-1.5 py-0.5 text-[10px] text-slate-600">
              {tabEmoji(q.tab)} {q.tab}
            </span>
          )}
        </div>
        <span className="text-[10px] text-slate-400">{q.id}</span>
      </div>

      <div className="space-y-1.5 px-3 py-2">
        <div>
          <div className="text-[10px] font-bold uppercase tracking-wide text-slate-400">Câu hỏi</div>
          <div className="text-sm text-slate-800 whitespace-pre-wrap break-words">{q.question}</div>
        </div>
        {isAnswered && q.answer && (
          <div className="rounded-md bg-emerald-50 px-2.5 py-1.5 ring-1 ring-emerald-100">
            <div className="text-[10px] font-bold uppercase tracking-wide text-emerald-700">
              Hermes · trả lời
            </div>
            <div className="text-sm text-slate-800 whitespace-pre-wrap break-words">{q.answer}</div>
          </div>
        )}
        <div className="text-[10px] text-slate-400">{q.created_at}</div>
      </div>
    </div>
  );
}

function tabEmoji(t: string): string {
  const m: Record<string, string> = {
    checklist: "✅",
    ingredients: "🛒",
    recipes: "🍝",
    budget: "💰",
    calendar: "📅",
  };
  return m[t] || "📌";
}
