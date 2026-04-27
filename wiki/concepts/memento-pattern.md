---
title: "Memento Pattern"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [design-patterns, behavioral-patterns, software-architecture, object-oriented, state-management]
---

# Memento Pattern

## Overview

The Memento Pattern is a behavioral design pattern that captures and externalizes an object's internal state so it can be restored later, without violating encapsulation. The pattern solves the problem of implementing undo mechanisms, checkpoints, and state rollback without exposing the object's internals to the rest of the system.

The name comes from the Latin "memento" meaning "remember"—the pattern creates snapshots of object state that can be remembered and restored later. This is essential for features like undo/redo in editors, transaction rollback in databases, checkpointing in games, and state recovery in long-running processes.

What makes the Memento Pattern elegant is its respect for encapsulation. The internal state of an object is often private precisely because it shouldn't be accessed directly by other objects. The Memento pattern works around this by having the Originator (the object whose state is being saved) create its own memento, containing exactly the state needed for restoration. The caretaker (typically an undo manager) stores and uses mementos without ever looking inside them.

## Key Concepts

**Originator** is the object whose state needs to be saved and restored. It creates a Memento containing a snapshot of its current state, and it accepts a Memento to restore its previous state. The originator knows exactly what state it needs to preserve—no more and no less.

**Memento** is a value object that stores the internal state of the Originator. It has two interfaces: a narrow interface for the caretaker (typically just "store this") and a wide interface for the originator (the ability to extract state for restoration). This asymmetry protects encapsulation while allowing state recovery.

**Caretaker** is responsible for the memento's safekeeping. It requests mementos from the originator and passes them back when restoration is needed. Caretakers never examine or modify the memento's contents—they simply hold them in storage (a stack for undo, a list for history, a file for persistence).

The pattern preserves encapsulation boundaries by ensuring the memento's internal structure is hidden from everything except the originator that created it. Other objects can request and store mementos, but they cannot access the state within them.

## How It Works

The Memento Pattern operates through a simple three-role interaction:

1. **Save**: The caretaker requests a memento from the originator. The originator creates a new memento object containing its current state and returns it to the caretaker. At this point, the caretaker holds the snapshot but cannot see inside it.

2. **Store**: The caretaker places the memento into its storage mechanism—a stack for undo operations, a list for versioning, a file for persistence. The memento remains inert, simply existing until needed.

3. **Restore**: When the caretaker needs to revert to a previous state, it passes the stored memento back to the originator. The originator extracts the state and uses it to reset its internal fields to the saved values.

This cycle can repeat indefinitely. For undo systems, the caretaker typically maintains a stack where pushing saves state and popping restores it. For checkpointing, the caretaker might periodically save mementos to persistent storage so state survives application restarts.

The key guarantee is that the external world never sees the originator's internals. If you implement undo via direct field access, you're violating encapsulation and inviting bugs. The memento pattern maintains the boundary while still enabling state recovery.

## Practical Applications

The Memento Pattern appears in systems requiring state recovery:

**Text Editors** - When you type in a word processor, each action might create a memento. The undo stack holds these mementos, and Ctrl+Z pops the most recent one to restore the previous state. This works even for complex edits like find-and-replace.

**Database Transactions** - Before applying changes, some systems save a memento of the pre-transaction state. If the transaction fails or is rolled back, the memento restores the original state.

**Games** - Many games include checkpoint systems that save game state (player position, inventory, quest progress) as mementos. If the player dies, they restart from the checkpoint rather than the beginning.

**State Machines** - Workflow engines and state machine implementations use mementos to save current state, allowing complex workflows to pause and resume without losing context.

**Configuration Management** - Applications often save configuration mementos before applying changes, enabling rollback to known-good states if new settings cause problems.

## Examples

```python
from dataclasses import dataclass, field
from typing import Any
from datetime import datetime

# Memento - stores internal state
class EditorMemento:
    def __init__(self, content: str, cursor_position: int, timestamp: datetime):
        self._content = content
        self._cursor_position = cursor_position
        self._timestamp = timestamp
    
    # Narrow interface for caretaker - no state access
    def get_stored_time(self) -> datetime:
        return self._timestamp
    
    # Wide interface for originator - state access
    def get_content(self) -> str:
        return self._content
    
    def get_cursor_position(self) -> int:
        return self._cursor_position

# Originator - creates and restores mementos
class TextEditor:
    def __init__(self):
        self._content = ""
        self._cursor_position = 0
    
    def type(self, text: str):
        self._content = self._content[:self._cursor_position] + text + self._content[self._cursor_position:]
        self._cursor_position += len(text)
    
    def move_cursor(self, position: int):
        self._cursor_position = max(0, min(position, len(self._content)))
    
    def get_state(self) -> str:
        return f"[{self._cursor_position}] {self._content}"
    
    # Create memento with current state
    def save(self) -> EditorMemento:
        return EditorMemento(self._content, self._cursor_position, datetime.now())
    
    # Restore from memento
    def restore(self, memento: EditorMemento):
        self._content = memento.get_content()
        self._cursor_position = memento.get_cursor_position()

# Caretaker - manages memento storage
class HistoryManager:
    def __init__(self, editor: TextEditor):
        self._editor = editor
        self._mementos: list[EditorMemento] = []
    
    def backup(self):
        self._mementos.append(self._editor.save())
        print(f"Saved state at {datetime.now()}")
    
    def undo(self):
        if not self._mementos:
            print("Nothing to undo")
            return
        memento = self._mementos.pop()
        self._editor.restore(memento)
        print(f"Restored to: {memento.get_stored_time()}")

# Usage
editor = TextEditor()
history = HistoryManager(editor)

editor.type("Hello ")
print(f"After 'Hello': {editor.get_state()}")

history.backup()

editor.type("World!")
print(f"After 'World!': {editor.get_state()}")

history.backup()

editor.type("There")
print(f"After 'There': {editor.get_state()}")

print("\n--- Undo ---")
history.undo()
print(f"After undo: {editor.get_state()}")

history.undo()
print(f"After undo: {editor.get_state()}")
```

## Related Concepts

- [[Design Patterns]] - The broader category of reusable software solutions
- [[Command Pattern]] - Often used together; commands create mementos as part of undo functionality
- [[Iterator Pattern]] - Mementos can serve as iterator snapshots for state iteration
- [[State Pattern]] - State objects can create mementos to enable state transitions
- [[Snapshot Isolation]] - Database concept related to state snapshots

## Further Reading

- Gamma, Erich, et al. "Design Patterns: Elements of Reusable Object-Oriented Software" (GoF)
- "Head First Design Patterns" by Freeman & Robson
- Database transaction management literature

## Personal Notes

The Memento Pattern works best when state snapshots are small. For large objects, consider incremental mementos or storing diffs rather than complete snapshots. I've also found that combining memento with command pattern creates a robust undo system—commands know what changes they made, so they can help construct targeted mementos. The main pitfall is forgetting that mementos should be immutable once created. If you let caretakers modify mementos, you lose the "time capsule" property that makes the pattern reliable.
