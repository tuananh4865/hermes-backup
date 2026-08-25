"use client";

import { useState } from "react";
import POS from "./POS";

export default function POSFloatingButton() {
  const [open, setOpen] = useState(false);

  return (
    <>
      {/* Floating Action Button — luôn hiện ở mọi tab */}
      <button
        onClick={() => setOpen(true)}
        className="fixed bottom-6 left-6 z-40 flex h-14 w-14 items-center justify-center rounded-full bg-emerald-500 text-2xl text-white shadow-2xl ring-4 ring-emerald-100 transition hover:scale-110 hover:bg-emerald-600"
        title="Bán hàng nhanh"
      >
        🛒
      </button>

      {/* Popup POS */}
      {open && (
        <div
          className="fixed inset-0 z-50 flex items-end bg-black/40 sm:items-center sm:justify-center"
          onClick={() => setOpen(false)}
        >
          <div
            className="max-h-[90vh] w-full overflow-y-auto rounded-t-2xl bg-slate-50 p-4 shadow-2xl sm:max-w-md sm:rounded-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <POS onClose={() => setOpen(false)} />
          </div>
        </div>
      )}
    </>
  );
}