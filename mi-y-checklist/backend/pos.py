"""
POS endpoints: Tạo đơn hàng từ POS → tự ghi vào orders.md
+ Edit cost trong cost.md
"""
import re
import secrets
import time
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal

router = APIRouter()

VAULT_ROOT = Path("/Volumes/Storage-1/Hermes/wiki/projects")


# ---------- Schemas ----------
class POSItem(BaseModel):
    menu: Literal["1A", "1B"]
    size: Literal["LỚN", "NHỎ"]
    quantity: int = 1


# Friendly display name
MENU_DISPLAY = {
    "1A": "Mì Ý Sốt Bò Bằm",
    "1B": "Mì Ý Sốt Kem",
}


class POSOrderCreate(BaseModel):
    customer: str
    phone: str
    address: str = ""
    items: list[POSItem]
    shipping: int = 0
    payment: str = "Tiền mặt"
    note: str = ""


class CostCellUpdate(BaseModel):
    row: int       # 0-based row index in the cost table (after header)
    col: str       # column header, e.g. "Cost (L)"
    value: str     # new value as string


# ---------- Price table ----------
PRICE = {
    ("1A", "LỚN"): 35000,
    ("1A", "NHỎ"): 30000,
    ("1B", "LỚN"): 45000,
    ("1B", "NHỎ"): 38000,
}


def calc_order_total(items: list[POSItem], shipping: int) -> tuple[int, list[str]]:
    """Return (subtotal, [lines])."""
    lines = []
    subtotal = 0
    for it in items:
        unit = PRICE[(it.menu, it.size)]
        sub = unit * it.quantity
        subtotal += sub
        lines.append(f"  - 1{item.menu} {it.size} x{it.quantity} = {sub:,}đ")
    return subtotal + shipping, lines


def file_path(slug: str, file: str) -> Path:
    return VAULT_ROOT / slug / f"{file}.md"


# ---------- ORD counter ----------
def next_order_seq(slug: str) -> int:
    """Read orders.md and find next sequence number for today."""
    p = file_path(slug, "orders")
    if not p.exists():
        return 1
    today = datetime.now().strftime("%Y%m%d")
    pattern = re.compile(rf"### ORD-{today}-(\d{{3,}})")
    max_n = 0
    for m in pattern.finditer(p.read_text()):
        n = int(m.group(1))
        if n > max_n:
            max_n = n
    return max_n + 1


def append_order_to_file(slug: str, order_md: str) -> None:
    """Append new order block to orders.md under weekly section."""
    p = file_path(slug, "orders")
    if not p.exists():
        p.write_text(f"# Orders\n\n{order_md}\n")
        return

    content = p.read_text()
    today = datetime.now()
    week_label = today.strftime("%d/%m")
    week_header_pattern = re.compile(
        rf"## Đơn tuần này \({today.strftime('%d/%m')}.*?\n"
    )

    if week_header_pattern.search(content):
        new_content = week_header_pattern.sub(
            lambda m: m.group(0) + "\n" + order_md + "\n",
            content,
            count=1,
        )
    else:
        new_section = f"\n## Đơn tuần này ({week_label}-...{today.strftime('%d/%m/%Y')})\n\n{order_md}\n"
        new_content = content + new_section

    p.write_text(new_content)


def save_customer(slug: str, name: str, phone: str, address: str, order_id: str) -> None:
    """Append customer to customers.md or update existing."""
    p = file_path(slug, "customers")
    today = datetime.now().strftime("%Y-%m-%d")

    if not p.exists():
        p.write_text(f"""---
title: Danh sách khách hàng
project: {slug}
type: customers
last_modified: {today}
---

# 👥 Danh sách khách hàng

| Tên | SĐT | Địa chỉ | Lần cuối | Số đơn | Đơn gần nhất |
|---|---|---|---|---:|---|
| {name} | {phone} | {address or "(không)"} | {today} | 1 | {order_id} |
""")
        return

    content = p.read_text()
    # Find table row by phone
    pattern = re.compile(rf"^\| (.+?) \| {re.escape(phone)} \|", re.MULTILINE)
    m = pattern.search(content)

    if m:
        # Update existing customer
        # Extract old name (group 1)
        old_line_start = m.start()
        old_line_end = content.find("\n", old_line_start)
        old_line = content[old_line_start:old_line_end]

        # Parse to update count + last order
        cells = [c.strip() for c in old_line.strip("|").split("|")]
        try:
            old_count = int(cells[4]) if len(cells) > 4 else 0
        except (ValueError, IndexError):
            old_count = 0
        new_count = old_count + 1

        new_line = f"| {cells[0]} | {phone} | {cells[2]} | {today} | {new_count} | {order_id} |"
        content = content[:old_line_start] + new_line + content[old_line_end:]
    else:
        # Add new customer row
        new_row = f"\n| {name} | {phone} | {address or '(không)'} | {today} | 1 | {order_id} |"
        # Insert before the next "## " section after the table
        table_end = content.find("\n\n", content.find("|----"))
        if table_end == -1:
            table_end = len(content)
        content = content[:table_end] + new_row + content[table_end:]

    p.write_text(content)


def find_customer_by_phone(slug: str, phone: str) -> dict | None:
    """Find customer in customers.md by phone."""
    p = file_path(slug, "customers")
    if not p.exists():
        return None
    content = p.read_text()
    pattern = re.compile(rf"^\| (.+?) \| {re.escape(phone)} \| (.+?) \| (.+?) \| (\d+) \| (ORD-[\w-]+) \|", re.MULTILINE)
    m = pattern.search(content)
    if not m:
        return None
    return {
        "name": m.group(1).strip(),
        "phone": phone,
        "address": m.group(2).strip(),
        "last_visit": m.group(3).strip(),
        "order_count": int(m.group(4)),
        "last_order_id": m.group(5),
    }


# ---------- Routes ----------
@router.post("/api/projects/{slug}/orders")
def create_order(slug: str, body: POSOrderCreate):
    if not body.items:
        raise HTTPException(400, "Đơn phải có ít nhất 1 món")

    seq = next_order_seq(slug)
    today = datetime.now().strftime("%Y%m%d")
    order_id = f"ORD-{today}-{seq:03d}"
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    subtotal_lines = []
    total = 0
    for it in body.items:
        unit = PRICE[(it.menu, it.size)]
        sub = unit * it.quantity
        total += sub
        subtotal_lines.append(f"  - {MENU_DISPLAY[it.menu]} {it.size} x{it.quantity} = {sub:,}đ")
    total += body.shipping

    order_md = f"""### {order_id}
- Ngày tạo: {now_str}
- Khách: {body.customer} — {body.phone}
- Địa chỉ: {body.address or '(không có)'}
- Món:
{chr(10).join(subtotal_lines)}
- Subtotal: {total - body.shipping:,}đ
- Phí ship: {body.shipping:,}đ
- Tổng: {total:,}đ
- Payment: {body.payment}
- Trạng thái: pending
- Ghi chú: {body.note or '(không có)'}
"""

    append_order_to_file(slug, order_md)
    save_customer(slug, body.customer, body.phone, body.address, order_id)

    return {
        "ok": True,
        "order_id": order_id,
        "total": total,
        "created_at": now_str,
    }


@router.get("/api/projects/{slug}/customers")
def list_customers(slug: str):
    """List all customers + their stats."""
    p = file_path(slug, "customers")
    if not p.exists():
        return {"customers": [], "count": 0}

    content = p.read_text()
    customers = []
    # Find rows in main table
    pattern = re.compile(
        r"^\| (.+?) \| (\+?\d[\d\s-]+) \| (.+?) \| (\d{4}-\d{2}-\d{2}) \| (\d+) \| (ORD-[\w-]+) \|",
        re.MULTILINE,
    )
    for m in pattern.finditer(content):
        customers.append({
            "name": m.group(1).strip(),
            "phone": m.group(2).strip(),
            "address": m.group(3).strip(),
            "last_visit": m.group(4),
            "order_count": int(m.group(5)),
            "last_order_id": m.group(6),
        })

    # Sort by order_count desc (khách thân trước)
    customers.sort(key=lambda c: -c["order_count"])

    return {"customers": customers, "count": len(customers)}


@router.get("/api/projects/{slug}/customers/lookup")
def lookup_customer(slug: str, phone: str):
    """Lookup customer by phone number."""
    customer = find_customer_by_phone(slug, phone)
    if not customer:
        return {"found": False}
    return {"found": True, "customer": customer}


@router.get("/api/projects/{slug}/menu")
def get_menu(slug: str):
    return {"items": [
        {"menu": k[0], "size": k[1], "price": v}
        for k, v in PRICE.items()
    ]}


@router.patch("/api/projects/{slug}/cost/update")
def update_cost_cell(slug: str, body: CostCellUpdate):
    """Update a single cell in cost.md table."""
    p = file_path(slug, "cost")
    if not p.exists():
        raise HTTPException(404, "cost.md not found")

    content = p.read_text()
    lines = content.split("\n")

    # Find cost table headers (line starting with "| Nguyên liệu" or similar)
    table_started = False
    table_lines = []
    for i, line in enumerate(lines):
        if line.startswith("|") and "Đơn giá" in line:
            table_started = True
            header_line = i
            continue
        if table_started and line.startswith("|---"):
            sep_line = i
            break
    else:
        raise HTTPException(400, "Cost table not found")

    # Get header column → index
    headers = [c.strip() for c in lines[header_line].strip("|").split("|")]
    try:
        col_idx = headers.index(body.col)
    except ValueError:
        raise HTTPException(400, f"Column '{body.col}' not in {headers}")

    # Find target row (row is 0-based data row)
    target_row = sep_line + 1 + body.row
    if target_row >= len(lines) or not lines[target_row].startswith("|"):
        raise HTTPException(400, f"Row {body.row} out of range")

    # Replace cell at col_idx
    cells = [c.strip() for c in lines[target_row].strip("|").split("|")]
    if col_idx >= len(cells):
        raise HTTPException(400, "Column index out of range")
    cells[col_idx] = body.value
    lines[target_row] = "| " + " | ".join(cells) + " |"

    p.write_text("\n".join(lines))
    return {"ok": True, "row": body.row, "col": body.col, "value": body.value}
