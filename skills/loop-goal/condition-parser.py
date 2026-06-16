#!/usr/bin/env python3
"""
Condition Parser — Parse và evaluate stopping conditions cho /goal primitive.

Hỗ trợ:
- Simple boolean: "output_score >= 9.0"
- Quality-checker verdict: "checker_verdict == PASS"
- Python expression (sandboxed): "output.engagement > 0.8"
"""
import ast
import sys
import json
import operator
from typing import Any, Dict


# Safe operators (no eval risk)
SAFE_OPS = {
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.And: lambda a, b: a and b,
    ast.Or: lambda a, b: a or b,
    ast.Not: operator.not_,
    ast.In: lambda a, b: a in b,
    ast.NotIn: lambda a, b: a not in b,
}


class SafeEvaluator:
    """Safely evaluate boolean conditions with whitelist."""

    def __init__(self, context: Dict[str, Any]):
        self.context = context

    def evaluate(self, expression: str) -> bool:
        """Evaluate a condition expression safely."""
        try:
            tree = ast.parse(expression, mode="eval")
            result = self._eval_node(tree.body)
            return bool(result)
        except Exception as e:
            print(f"⚠️  Condition parse error: {e}")
            return False

    def _eval_node(self, node):
        """Recursively evaluate AST nodes (whitelist only)."""
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Name):
            if node.id not in self.context:
                raise NameError(f"Variable '{node.id}' not in context")
            return self.context[node.id]
        if isinstance(node, ast.Attribute):
            # For nested attribute access like output.engagement
            value = self._eval_node(node.value)
            if isinstance(value, dict):
                return value.get(node.attr)
            return getattr(value, node.attr, None)
        if isinstance(node, ast.Compare):
            left = self._eval_node(node.left)
            for op, comparator in zip(node.ops, node.comparators):
                op_type = type(op)
                if op_type not in SAFE_OPS:
                    raise ValueError(f"Operator {op_type.__name__} not allowed")
                right = self._eval_node(comparator)
                if not SAFE_OPS[op_type](left, right):
                    return False
                left = right
            return True
        if isinstance(node, ast.BoolOp):
            values = [self._eval_node(v) for v in node.values]
            op_type = type(node.op)
            if op_type == ast.And:
                return all(values)
            if op_type == ast.Or:
                return any(values)
        if isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.Not):
                return not self._eval_node(node.operand)
        raise TypeError(f"Unsupported AST node: {type(node).__name__}")


def parse_quality_checker_output(verdict_dict: Dict) -> Dict[str, Any]:
    """Convert quality-checker verdict to flat context for conditions."""
    return {
        "checker_verdict": verdict_dict.get("verdict", "FAIL"),
        "checker_score": verdict_dict.get("score", 0),
        "has_critical": any(
            i.get("severity") == "critical"
            for i in verdict_dict.get("issues", [])
        ),
        "n_issues": len(verdict_dict.get("issues", [])),
        "issues": verdict_dict.get("issues", []),
    }


# === CLI ===
if __name__ == "__main__" and len(sys.argv) > 1:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", nargs=2, metavar=("VERDICT", "SCORE"))
    parser.add_argument("--condition", required=True)
    parser.add_argument("--context", default="{}", help="JSON context")
    args = parser.parse_args()
    
    if args.check:
        verdict, score = args.check
        context = {
            "checker_verdict": verdict,
            "checker_score": float(score),
            "has_critical": False,  # assumed for CLI
            "n_issues": 0,
        }
        # Merge with additional context
        try:
            extra = json.loads(args.context)
            context.update(extra)
        except:
            pass
        
        ev = SafeEvaluator(context)
        result = ev.evaluate(args.condition)
        sys.exit(0 if result else 1)


# === Test ===

    print("🧪 Condition Parser — Test\n")
    
    # Test 1: Simple comparison
    ctx = {"output_score": 9.5, "verdict": "PASS"}
    ev = SafeEvaluator(ctx)
    tests = [
        ("output_score >= 9.0", True),
        ("output_score < 9.0", False),
        ("output_score == 9.5", True),
        ("verdict == 'PASS'", True),
        ("verdict == 'FAIL'", False),
    ]
    
    all_pass = True
    for expr, expected in tests:
        result = ev.evaluate(expr)
        status = "✅" if result == expected else "❌"
        if result != expected:
            all_pass = False
        print(f"{status} {expr} → {result} (expected {expected})")
    
    # Test 2: Complex boolean
    print("\n--- Complex boolean ---")
    ctx2 = {
        "checker_verdict": "PASS",
        "checker_score": 9.2,
        "has_critical": False,
    }
    ev2 = SafeEvaluator(ctx2)
    complex_tests = [
        ("checker_verdict == 'PASS' and checker_score >= 9.0", True),
        ("checker_verdict == 'PASS' and not has_critical", True),
        ("checker_verdict == 'FAIL' or has_critical", False),
    ]
    for expr, expected in complex_tests:
        result = ev2.evaluate(expr)
        status = "✅" if result == expected else "❌"
        if result != expected:
            all_pass = False
        print(f"{status} {expr} → {result} (expected {expected})")
    
    # Test 3: Safety — no dangerous code (must be BLOCKED, returning False is OK)
    print("\n--- Safety ---")
    dangerous = [
        "__import__('os').system('rm -rf /')",
        "open('/etc/passwd').read()",
        "eval('1+1')",
    ]
    all_blocked = True
    for expr in dangerous:
        try:
            result = ev.evaluate(expr)
            # For dangerous code, returning False is also "safe" (nothing executed)
            if result is False or result is None:
                print(f"✅ Blocked (returned {result}): {expr[:40]}...")
            else:
                print(f"❌ UNSAFE: {expr} returned {result}")
                all_blocked = False
        except Exception as e:
            # Good — dangerous code was blocked with exception
            print(f"✅ Blocked (exception): {expr[:40]}... ({type(e).__name__})")
    
    if not all_blocked:
        all_pass = False
    
    if all_pass:
        print("\n✅ All condition parser tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed")
        sys.exit(1)
