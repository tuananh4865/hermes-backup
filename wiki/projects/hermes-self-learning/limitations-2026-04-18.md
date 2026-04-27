---
title: "Hệ thống Self-Learning - Hạn chế hiện tại (2026-04-18)"
created: 2026-04-21
updated: 2026-04-21
type: project
tags: ['project']
---

# Hệ thống Self-Learning - Hạn chế hiện tại (2026-04-18)

## Tình trạng sau Phase 2 + P3: ✅ CORE LOOP + QUALITY + CONFIG + USER FEEDBACK COMPLETE

**Đã fix:**
- ✅ `save_trajectories=True` → AIAgent khởi tạo đủ bộ TrajectoryIndex + OutcomeEvaluator + ComplexityAnalyzer + PatternMatcher + ProactivePlanner
- ✅ Shared instance — tất cả dùng chung 1 TrajectoryIndex
- ✅ ProactivePlanner.plan_ahead() hook vào run_conversation() trước khi agent làm việc
- ✅ OutcomeEvaluator.evaluate() hook vào run_conversation() sau khi task kết thúc
- ✅ OutcomeEvaluator tự động index trajectory bên trong
- ✅ get_adjustment() trong TrajectoryIndex để ComplexityAnalyzer học từ history
- ✅ Config: `true` → `True` (Python boolean fix)
- ✅ P2.1: Inject recommended_actions vào user message (run_agent.py)
- ✅ P2.2: Show pattern warnings qua _emit_status lifecycle callback (run_agent.py)
- ✅ P2.3: Integration tests — 27 tests, all passing (tests/agent/test_self_learning.py)
- ✅ Bug fix: ComplexityAnalyzer.get_adjustment() giờ gọi trajectory_index.get_adjustment()
- ✅ Bug fix: ProactivePlanner early returns đã include đủ fields (adjusted_iteration_budget, abort_reason)
- ✅ P3.1: Config-driven complexity weights — `self_learning.complexity_weights` trong config.yaml
- ✅ P3.2: User-facing lesson feedback — `get_recent_lessons()` + `format_lessons_for_user()` emit qua `_emit_status`

---

## Hạn chế còn lại

### Hạn chế #5: Kết quả proactive planning chưa được dùng để adjust behavior

**Vấn đề:** `plan.adjusted_iteration_budget` và `plan.recommended_actions` được set nhưng:
- Iteration budget chỉ được adjust nếu proactive planner set nó (đã implement ✅)
- Recommended actions không ảnh hưởng đến agent behavior

**Fix:** Dùng `plan.recommended_actions` để inject hints vào system prompt hoặc điều chỉnh strategy.

---

### Hạn chế #6: Thiếu integration tests

**Vấn đề:** Không có test end-to-end cho flow đầy đủ.

**Fix:** Viết test trong `tests/agent/test_self_learning.py`.

---

### Hạn chế #7: Pattern warnings chưa được hiển thị cho user

**Vấn đề:** Warnings được log nhưng user không thấy trước khi agent làm việc.

**Fix:** Inject warnings vào proactive context hoặc hiển thị qua status callback.

---

## Priority Order cho fix còn lại

```
Phase 2 (Quality): ✅ COMPLETE
Phase 3 (Polish):
  P3.1: Config-driven complexity weights ✅ COMPLETE
  P3.2: User-facing feedback về learned lessons ✅ COMPLETE
```

---

## Rủi ro đã giảm

1. ~~Breaking change~~ — đã hook cẩn thận vào các điểm có guard `if self._outcome_evaluator is not None`
2. ~~Performance~~ — proactive planning chạy synchronous nhưng có try/except wrapper
3. ~~DB initialization~~ — TrajectoryIndex có try/except graceful fallback
4. ~~Subagent timeout~~ — ProactivePlanner có subagent_timeout 120s

## Đã xác minh hoạt động

- ✅ Import tất cả module thành công
- ✅ AIAgent import không lỗi
- ✅ Shared TrajectoryIndex instance hoạt động
- ✅ OutcomeEvaluator.evaluate() tự index không double-call
