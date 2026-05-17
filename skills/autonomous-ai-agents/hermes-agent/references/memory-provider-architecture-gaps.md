# WikiMemoryProvider Architecture Gaps (2026-05-17)

## Tổng Quan

WikiMemoryProvider (`~/.hermes/plugins/memory/wiki/__init__.py`, 1458 lines) implement full active-write memory loop, NHƯNG có 3 gaps kiến trúc nghiêm trọng:

## Gap 1: `on_session_switch()` Được Định Nghĩa Nhưng Không Được Gọi

**Vị trí:** `agent/memory_manager.py:403-436`

```python
def on_session_switch(self, new_session_id: str, *, parent_session_id: str = "", reset: bool = False, **kwargs) -> None:
    """Notify all providers that the agent's session_id has rotated."""
```

**Vấn đề:** Method được định nghĩa TRONG `MemoryManager` và cả trong `WikiMemoryProvider` (stub), nhưng `run_agent.py` **KHÔNG BAO GIỜ GỌI** nó khi `session_id` thay đổi trong `_compress_context()`.

**Tại sao quan trọng:** Khi context compression xảy ra:
```python
# run_agent.py ~line 10734
self.session_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
os.environ["HERMES_SESSION_ID"] = self.session_id
```
Session ID thay đổi nhưng WikiMemoryProvider không được notify — nó tiếp tục write vào checkpoint file với session ID cũ.

**Fix cần thiết:** Thêm vào `run_agent.py` sau khi session_id thay đổi:
```python
if self._memory_manager:
    self._memory_manager.on_session_switch(self.session_id, parent_session_id=old_session_id)
```

## Gap 2: `on_post_compress()` Không Tồn Tại

**Vấn đề:** Có `on_pre_compress()` (ghi checkpoint TRƯỚC compress) nhưng không có `on_post_compress()` (đọc lại checkpoint SAU compress để restore context).

**Luồng hiện tại:**
```
on_pre_compress() → ghi pre_compact_{session}.md
compress() → context bị压缩
[SESSION MỚI BẮT ĐẦU] → model không có checkpoint data
```

**Fix cần thiết:** 
1. Thêm `WikiMemoryProvider.on_post_compress(old_session_id, compressed_messages)` 
2. Thêm `MemoryManager.on_post_compress()`
3. Gọi từ `run_agent._compress_context()` sau khi compression xong

## Gap 3: Proactive Retrieval Chỉ Chạy Khi Có User Query

**Vấn đề:** `prefetch()` chỉ được gọi khi user gửi message. Giữa các turn, không có proactive recall từ checkpoint.

**Hiện tại có:**
- `sync_turn()` — mỗi turn
- `on_pre_compress()` — write checkpoint
- `on_session_end()` — flush
- `prefetch(query)` — only triggered by user message

**Thiếu:**
- Proactive `_proactive_retrieve()` đọc checkpoint và tự động query wiki mà không cần user trigger

## Memory Lifecycle Hiện Tại (CÓ Issues)

```
initialize()
    ↓
sync_turn() ← mỗi turn
    ↓
_sync_fact_realtime() ← real-time write MEMORY.md ✅
    ↓
CHECKPOINT_EVERY_N_TURNS → _trigger_rolling_checkpoint() ✅
    ↓
on_pre_compress() ← context compression TRƯỚC ✅
    ↓
[COMPRESSION XẢY RA]
    ↓
session_id thay đổi ← on_session_switch() KHÔNG ĐƯỢC GỌI ❌
    ↓
model tiếp tục với SUMMARY_PREFIX ← on_post_compress() KHÔNG TỒN TẠI ❌
    ↓
on_session_end() ← session kết thúc ✅
```

## Files Quan Trọng

| File | Lines | Mô tả |
|------|-------|-------|
| `~/.hermes/plugins/memory/wiki/__init__.py` | 1458 | Full WikiMemoryProvider |
| `agent/memory_manager.py` | 555 | MemoryManager orchestration |
| `run_agent.py:10656` | — | `_compress_context()` |
| `agent/context_compressor.py` | 1583 | Context compression logic |

## Verification Steps

Để verify gaps trên:
```bash
# Gap 1: Search for on_session_switch calls
grep -n "on_session_switch" ~/.hermes/hermes-agent/run_agent.py
# Kết quả: KHÔNG CÓ — gap confirmed

# Gap 2: Search for on_post_compress
grep -n "on_post_compress" ~/.hermes/hermes-agent/run_agent.py
# Kết quả: KHÔNG CÓ — gap confirmed

# Xem WikiMemoryProvider methods
grep -n "def on_" ~/.hermes/plugins/memory/wiki/__init__.py
# Có: on_pre_compress, on_session_end, on_turn_start
# Không có: on_post_compress, on_session_switch
```

## Implementation Sequence Đề Xuất

| Phase | Action | Effort |
|-------|--------|--------|
| 1 | Add `on_session_switch()` call in `run_agent._compress_context()` | 15 min |
| 2 | Add `WikiMemoryProvider.on_post_compress()` + `MemoryManager.on_post_compress()` | 30 min |
| 3 | Add proactive retrieval via `_proactive_retrieve()` | 45 min |
| 4 | Semantic health check (self-maintenance) | 60+ min |