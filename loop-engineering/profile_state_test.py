#!/usr/bin/env python3
"""Test profile_state.py — verify HERMES_HOME-aware state management."""
import sys
import os
import shutil
import tempfile
from pathlib import Path

# Test setup: use a temp HERMES_HOME
TEST_HERMES_HOME = tempfile.mkdtemp(prefix="hermes_test_")
os.environ["HERMES_HOME"] = TEST_HERMES_HOME

# Re-import with new HERMES_HOME
sys.path.insert(0, "/Users/tuananh4865/.hermes/loop-engineering")
import importlib
import profile_state
importlib.reload(profile_state)

print("🧪 Profile State Helper — Test Suite")
print("=" * 60)
print(f"   Test HERMES_HOME: {TEST_HERMES_HOME}")
print()

PASS = 0
FAIL = 0

# Test 1: ensure_state creates file from template
print("Test 1: ensure_state creates file from template")
profile_state.ensure_state("test-profile-1")
expected = Path(TEST_HERMES_HOME) / "profiles" / "test-profile-1" / "state.md"
if expected.exists():
    print(f"  ✅ PASS — {expected}")
    PASS += 1
else:
    print(f"  ❌ FAIL — file not created")
    FAIL += 1

# Test 2: state file has correct content
print("\nTest 2: state file contains profile name")
content = expected.read_text()
if "test-profile-1" in content:
    print(f"  ✅ PASS — profile name in content")
    PASS += 1
else:
    print(f"  ❌ FAIL — profile name missing")
    FAIL += 1

# Test 3: append_verdict adds row
print("\nTest 3: append_verdict adds row")
profile_state.append_verdict(
    "test-profile-1", "PASS", 9.3, [], goal="Test goal", worker="test-profile-1"
)
content = expected.read_text()
if "| PASS | 9.3 |" in content:
    print(f"  ✅ PASS — verdict row added")
    PASS += 1
else:
    print(f"  ❌ FAIL — verdict row missing")
    print(f"  Content: {content[:500]}")
    FAIL += 1

# Test 4: append_run adds row
print("\nTest 4: append_run adds row")
profile_state.append_run("test-profile-1", "Test goal", 3, "PASS", 9.3)
content = expected.read_text()
if "| Test goal | test-profile-1 | 3 | PASS | 9.3 |" in content:
    print(f"  ✅ PASS — run row added")
    PASS += 1
else:
    print(f"  ❌ FAIL — run row missing")
    FAIL += 1

# Test 5: list_profiles returns list
print("\nTest 5: list_profiles returns list")
profiles = profile_state.list_profiles()
if "test-profile-1" in profiles:
    print(f"  ✅ PASS — {profiles}")
    PASS += 1
else:
    print(f"  ❌ FAIL — test-profile-1 not in {profiles}")
    FAIL += 1

# Test 6: state_path is HERMES_HOME-aware
print("\nTest 6: state_path respects HERMES_HOME")
sp = profile_state.state_path("foo")
expected_path = Path(TEST_HERMES_HOME) / "profiles" / "foo" / "state.md"
if sp == expected_path:
    print(f"  ✅ PASS — {sp}")
    PASS += 1
else:
    print(f"  ❌ FAIL — got {sp}, expected {expected_path}")
    FAIL += 1

# Test 7: ensure for different profile
print("\nTest 7: ensure works for multiple profiles")
profile_state.ensure_state("test-profile-2")
profile_state.ensure_state("test-profile-3")
all_profiles = profile_state.list_profiles()
if "test-profile-2" in all_profiles and "test-profile-3" in all_profiles:
    print(f"  ✅ PASS — {all_profiles}")
    PASS += 1
else:
    print(f"  ❌ FAIL — missing profiles")
    FAIL += 1

# Cleanup
shutil.rmtree(TEST_HERMES_HOME, ignore_errors=True)
os.environ.pop("HERMES_HOME", None)

print()
print("=" * 60)
print(f"📊 Results: {PASS} passed, {FAIL} failed")
print("=" * 60)

if FAIL == 0:
    print("✅ All tests passed!")
    sys.exit(0)
else:
    print("❌ Some tests failed")
    sys.exit(1)
