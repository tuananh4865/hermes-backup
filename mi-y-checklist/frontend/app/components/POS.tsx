"use client";

import { useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:7891";
const SLUG = "mi-y-kontum-research";

type MenuItem = {
  menu: "1A" | "1B";
  size: string;
  price: number;
  name: string;
};

const FEATURED: MenuItem[] = [
  { menu: "1A", size: "LỚN", price: 35000, name: "Mì Ý Sốt Bò Bằm" },
  { menu: "1A", size: "NHỎ", price: 30000, name: "Mì Ý Sốt Bò Bằm" },
  { menu: "1B", size: "LỚN", price: 45000, name: "Mì Ý Sốt Kem" },
  { menu: "1B", size: "NHỎ", price: 38000, name: "Mì Ý Sốt Kem" },
];

type CartLine = MenuItem & { quantity: number };

type Customer = {
  name: string;
  phone: string;
  address: string;
  last_visit: string;
  order_count: number;
  last_order_id: string;
};

export default function POS({ onClose }: { onClose?: () => void }) {
  const [cart, setCart] = useState<CartLine[]>([]);
  const [customer, setCustomer] = useState("");
  const [phone, setPhone] = useState("");
  const [address, setAddress] = useState("");
  const [shipping, setShipping] = useState(0);
  const [payment, setPayment] = useState("Tiền mặt");
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<{ order_id: string; total: number; customer: Customer | null } | null>(null);
  const [showCustomerPicker, setShowCustomerPicker] = useState(false);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [phoneLookup, setPhoneLookup] = useState<Customer | null>(null);

  function addItem(item: MenuItem) {
    setCart((prev) => {
      const existing = prev.find((l) => l.menu === item.menu && l.size === item.size);
      if (existing) {
        return prev.map((l) =>
          l.menu === item.menu && l.size === item.size
            ? { ...l, quantity: l.quantity + 1 }
            : l
        );
      }
      return [...prev, { ...item, quantity: 1 }];
    });
  }

  function removeItem(idx: number) {
    setCart((prev) => prev.filter((_, i) => i !== idx));
  }

  function adjustQty(idx: number, delta: number) {
    setCart((prev) =>
      prev
        .map((l, i) => (i === idx ? { ...l, quantity: Math.max(0, l.quantity + delta) } : l))
        .filter((l) => l.quantity > 0)
    );
  }

  const subtotal = cart.reduce((sum, l) => sum + l.price * l.quantity, 0);
  const total = subtotal + shipping;

  async function openCustomerPicker() {
    setShowCustomerPicker(true);
    try {
      const r = await fetch(`${API_BASE}/api/projects/${SLUG}/customers`);
      const data = await r.json();
      setCustomers(data.customers || []);
    } catch (e) {
      console.error(e);
    }
  }

  function pickCustomer(c: Customer) {
    setCustomer(c.name);
    setPhone(c.phone);
    setAddress(c.address !== "(không)" ? c.address : "");
    setShowCustomerPicker(false);
    setPhoneLookup(c);
  }

  async function lookupPhone(value: string) {
    setPhone(value);
    if (value.length < 9) {
      setPhoneLookup(null);
      return;
    }
    try {
      const r = await fetch(`${API_BASE}/api/projects/${SLUG}/customers/lookup?phone=${encodeURIComponent(value)}`);
      const data = await r.json();
      if (data.found) {
        setPhoneLookup(data.customer);
        // Auto-fill if new phone but no name yet
        if (!customer) {
          setCustomer(data.customer.name);
          if (data.customer.address && data.customer.address !== "(không)") {
            setAddress(data.customer.address);
          }
        }
      } else {
        setPhoneLookup(null);
      }
    } catch (e) {
      console.error(e);
    }
  }

  async function submit() {
    if (!customer.trim() || !phone.trim()) {
      alert("Vui lòng nhập tên + SĐT khách");
      return;
    }
    if (cart.length === 0) {
      alert("Giỏ hàng trống");
      return;
    }

    setBusy(true);
    try {
      const resp = await fetch(`${API_BASE}/api/projects/${SLUG}/orders`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          customer,
          phone,
          address,
          shipping,
          payment,
          note,
          items: cart.map((l) => ({ menu: l.menu, size: l.size, quantity: l.quantity })),
        }),
      });
      const data = await resp.json();
      if (data.ok) {
        setResult({
          order_id: data.order_id,
          total: data.total,
          customer: phoneLookup,
        });
        setCart([]);
        setCustomer("");
        setPhone("");
        setAddress("");
        setShipping(0);
        setNote("");
        setPhoneLookup(null);
      } else {
        alert("Lỗi: " + JSON.stringify(data));
      }
    } catch (e) {
      alert("Lỗi kết nối: " + String(e));
    } finally {
      setBusy(false);
    }
  }

  // RESULT SCREEN
  if (result) {
    return (
      <div className="rounded-2xl bg-white p-6 shadow-sm">
        <div className="flex h-16 w-16 mx-auto items-center justify-center rounded-full bg-green-100">
          <span className="text-3xl">✅</span>
        </div>
        <h2 className="mt-4 text-center text-xl font-bold text-slate-800">
          Đơn hàng đã tạo!
        </h2>
        <div className="mt-4 space-y-2 rounded-xl bg-slate-50 p-4">
          <div className="flex justify-between text-sm">
            <span className="text-slate-500">Mã đơn</span>
            <span className="font-mono font-bold text-slate-800">{result.order_id}</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-slate-500">Khách</span>
            <span className="font-medium text-slate-800">{result.customer?.name || "Khách mới"}</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-slate-500">Số đơn KH</span>
            <span className="font-bold text-emerald-600">
              {result.customer ? `#${result.customer.order_count}` : "1"}
            </span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-slate-500">Tổng tiền</span>
            <span className="font-bold text-green-600">{result.total.toLocaleString("vi-VN")}đ</span>
          </div>
        </div>
        <button
          onClick={() => setResult(null)}
          className="mt-6 w-full rounded-xl bg-slate-900 py-3 text-sm font-medium text-white hover:bg-slate-800"
        >
          + Tạo đơn mới
        </button>
        {onClose && (
          <button
            onClick={onClose}
            className="mt-2 w-full rounded-xl bg-slate-100 py-3 text-sm font-medium text-slate-600 hover:bg-slate-200"
          >
            Đóng
          </button>
        )}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Menu grid */}
      <div className="rounded-2xl bg-white p-4 shadow-sm">
        <h2 className="mb-3 text-sm font-bold text-slate-700">🍽️ Chọn món</h2>
        <div className="grid grid-cols-2 gap-2">
          {FEATURED.map((item) => (
            <button
              key={`${item.menu}-${item.size}`}
              onClick={() => addItem(item)}
              disabled={busy}
              className="rounded-xl border border-slate-200 bg-slate-50 p-3 text-left transition hover:border-emerald-300 hover:bg-emerald-50 disabled:opacity-50"
            >
              <div className="text-xs font-medium text-slate-500">{item.name}</div>
              <div className="text-sm font-bold text-slate-800">Size {item.size}</div>
              <div className="mt-1 text-sm font-bold text-emerald-600">
                {item.price.toLocaleString("vi-VN")}đ
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Cart */}
      <div className="rounded-2xl bg-white p-4 shadow-sm">
        <h2 className="mb-3 text-sm font-bold text-slate-700">🛒 Giỏ hàng ({cart.length})</h2>
        {cart.length === 0 ? (
          <div className="rounded-lg border-2 border-dashed border-slate-200 p-4 text-center text-sm text-slate-400">
            Chưa có món nào — bấm chọn món ở trên ↑
          </div>
        ) : (
          <ul className="divide-y divide-slate-100">
            {cart.map((l, idx) => (
              <li key={idx} className="flex items-center gap-2 py-2">
                <div className="flex-1">
                  <div className="text-sm font-bold text-slate-800">
                    {l.name} {l.size}
                  </div>
                  <div className="text-xs text-slate-500">
                    {l.price.toLocaleString("vi-VN")}đ × {l.quantity}
                  </div>
                </div>
                <div className="flex items-center gap-1">
                  <button
                    onClick={() => adjustQty(idx, -1)}
                    className="rounded-md border border-slate-200 px-2 text-slate-600 hover:bg-slate-100"
                  >
                    −
                  </button>
                  <span className="w-6 text-center text-sm font-bold">{l.quantity}</span>
                  <button
                    onClick={() => adjustQty(idx, +1)}
                    className="rounded-md border border-slate-200 px-2 text-slate-600 hover:bg-slate-100"
                  >
                    +
                  </button>
                </div>
                <button
                  onClick={() => removeItem(idx)}
                  className="ml-2 text-slate-300 hover:text-red-500"
                  title="Xóa"
                >
                  ✕
                </button>
              </li>
            ))}
          </ul>
        )}
        <div className="mt-3 space-y-1 border-t border-slate-100 pt-3">
          <div className="flex justify-between text-sm text-slate-500">
            <span>Tạm tính</span>
            <span>{subtotal.toLocaleString("vi-VN")}đ</span>
          </div>
          <div className="flex items-center justify-between text-sm text-slate-500">
            <span>Phí ship</span>
            <input
              type="number"
              value={shipping || ""}
              onChange={(e) => setShipping(Number(e.target.value) || 0)}
              placeholder="0"
              className="w-20 rounded border border-slate-200 px-2 py-0.5 text-right text-sm focus:border-slate-400 focus:outline-none"
            />
          </div>
          <div className="flex justify-between border-t border-slate-200 pt-2 text-base font-bold">
            <span>Tổng</span>
            <span className="text-emerald-600">{total.toLocaleString("vi-VN")}đ</span>
          </div>
        </div>
      </div>

      {/* Customer info */}
      <div className="rounded-2xl bg-white p-4 shadow-sm">
        <div className="mb-3 flex items-center justify-between">
          <h2 className="text-sm font-bold text-slate-700">👤 Thông tin khách</h2>
          <button
            onClick={openCustomerPicker}
            className="rounded-lg bg-blue-50 px-3 py-1 text-xs font-bold text-blue-600 hover:bg-blue-100"
          >
            📋 Chọn từ DS
          </button>
        </div>

        {phoneLookup && (
          <div className="mb-3 rounded-lg bg-amber-50 p-2 text-xs">
            <div className="font-bold text-amber-700">
              ⭐ Khách quen — đã {phoneLookup.order_count} đơn
            </div>
            <div className="text-amber-600">
              Đơn gần nhất: {phoneLookup.last_order_id}
            </div>
          </div>
        )}

        <div className="space-y-2">
          <input
            type="tel"
            placeholder="Số điện thoại * (gõ để tìm khách cũ)"
            value={phone}
            onChange={(e) => lookupPhone(e.target.value)}
            className="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm focus:border-slate-400 focus:outline-none"
          />
          <input
            type="text"
            placeholder="Tên khách hàng *"
            value={customer}
            onChange={(e) => setCustomer(e.target.value)}
            className="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm focus:border-slate-400 focus:outline-none"
          />
          <input
            type="text"
            placeholder="Địa chỉ giao (optional)"
            value={address}
            onChange={(e) => setAddress(e.target.value)}
            className="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm focus:border-slate-400 focus:outline-none"
          />
          <select
            value={payment}
            onChange={(e) => setPayment(e.target.value)}
            className="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm focus:border-slate-400 focus:outline-none"
          >
            <option>Tiền mặt</option>
            <option>CK Vietcombank</option>
            <option>MoMo</option>
            <option>ShopeeFood</option>
            <option>GrabFood</option>
          </select>
          <textarea
            placeholder="Ghi chú (ít cay, không hành...)"
            value={note}
            onChange={(e) => setNote(e.target.value)}
            rows={2}
            className="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm focus:border-slate-400 focus:outline-none"
          />
        </div>
      </div>

      {/* Submit */}
      <button
        onClick={submit}
        disabled={busy || cart.length === 0}
        className="w-full rounded-2xl bg-emerald-500 py-4 text-base font-bold text-white shadow-lg transition hover:bg-emerald-600 disabled:opacity-30"
      >
        {busy ? "Đang lưu..." : `🛒 Tạo đơn — ${total.toLocaleString("vi-VN")}đ`}
      </button>

      {onClose && (
        <button
          onClick={onClose}
          className="w-full rounded-xl bg-slate-100 py-3 text-sm font-medium text-slate-600 hover:bg-slate-200"
        >
          Đóng POS
        </button>
      )}

      {/* Customer picker modal */}
      {showCustomerPicker && (
        <div className="fixed inset-0 z-50 flex items-end bg-black/40 sm:items-center sm:justify-center" onClick={() => setShowCustomerPicker(false)}>
          <div
            className="max-h-[80vh] w-full overflow-y-auto rounded-t-2xl bg-white p-4 shadow-2xl sm:max-w-md sm:rounded-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="mb-3 flex items-center justify-between">
              <h3 className="text-base font-bold text-slate-800">📋 Khách hàng ({customers.length})</h3>
              <button onClick={() => setShowCustomerPicker(false)} className="text-slate-400">✕</button>
            </div>
            {customers.length === 0 ? (
              <div className="py-8 text-center text-sm text-slate-400">Chưa có khách nào</div>
            ) : (
              <ul className="divide-y divide-slate-100">
                {customers.map((c) => (
                  <li
                    key={c.phone}
                    onClick={() => pickCustomer(c)}
                    className="cursor-pointer rounded-lg px-3 py-2.5 hover:bg-blue-50"
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="text-sm font-bold text-slate-800">
                          {c.order_count >= 3 && "⭐ "}{c.name}
                        </div>
                        <div className="text-xs text-slate-500">{c.phone}</div>
                      </div>
                      <div className="text-right">
                        <div className="rounded-full bg-emerald-100 px-2 py-0.5 text-xs font-bold text-emerald-700">
                          {c.order_count} đơn
                        </div>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      )}
    </div>
  );
}