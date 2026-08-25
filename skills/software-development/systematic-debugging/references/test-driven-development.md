# Test-Driven Development Reference

Formerly a standalone skill. Content absorbed into `systematic-debugging`.

## TDD Cycle

```
1. RED: Write a failing test
2. GREEN: Write minimal code to pass
3. REFACTOR: Improve code while keeping tests green
```

## Python pytest Example

```python
def test_addition():
    assert add(2, 3) == 5

def add(a, b):
    return a + b  # minimal implementation
```

## Run Tests

```bash
pytest tests/ -v
pytest tests/ -v -k "test_name"
```
