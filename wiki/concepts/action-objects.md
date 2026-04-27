---
title: "Action Objects"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [design-patterns, object-oriented, architecture, game-development]
---

# Action Objects

## Overview

Action objects, also known as command objects, are a design pattern where requests or operations are encapsulated as standalone objects containing all information needed to execute an action. Instead of calling a method directly, you create an object that represents the intent ("MovePlayerToLocation"), stores the necessary parameters (player ID, destination coordinates), and knows how to execute itself. This indirection enables powerful capabilities: undo/redo functionality, queuing and scheduling of operations, logging and audit trails, and composition of complex operations from simpler ones.

The pattern appears across software domains but is particularly prominent in game development (where player actions, AI behaviors, and system commands are frequently modeled as objects), document editing applications (enabling the famous Ctrl+Z undo stack), and workflow engines (where business processes are modeled as chains of executable actions). The key insight is that by treating operations as first-class data, you gain the ability to introspect, serialize, defer, and recombine them in ways impossible with direct method calls.

## Key Concepts

**Encapsulation of Execution** is the core principle. An action object bundles the "what" (the operation type) with the "how" (parameters and execution logic) and sometimes the "before state" needed for undo. This bundle can be passed around, stored, inspected, and executed on demand. The receiver of an action object doesn't need to understand its internals — it just needs to know how to invoke it.

**Undo/Redo Support** emerges naturally from action objects because they can store the state before and after execution. An undoable action records both the initial state and the changes made, enabling reversal. Some implementations store only the initial state and the inverse operation; others store complete state snapshots. The trade-off is memory versus implementation complexity.

**Command Queuing and Scheduling** becomes possible when actions are objects. You can build queues of actions to execute later, schedule actions for specific times, implement macro systems where users string actions together, or add transactional semantics where a sequence of actions either all succeed or all roll back.

**Command History** provides an audit trail of operations performed. Because actions are objects, they can be logged, serialized, and replayed. This is invaluable for debugging, reproducing issues, and understanding system behavior over time.

## How It Works

A typical action object implementation follows this structure:

```python
# Base action object interface
from abc import ABC, abstractmethod
from typing import Any
import json

class Action(ABC):
    @abstractmethod
    def execute(self) -> Any:
        """Perform the action"""
        pass
    
    @abstractmethod
    def undo(self) -> None:
        """Reverse the action"""
        pass
    
    @abstractmethod
    def serialize(self) -> dict:
        """Convert action to storable format"""
        pass

# Concrete action implementation
class MovePlayerAction(Action):
    def __init__(self, player_id: str, destination: tuple[float, float]):
        self.player_id = player_id
        self.destination = destination
        self.previous_position = None
    
    def execute(self):
        # Store state for potential undo
        player = get_player(self.player_id)
        self.previous_position = (player.x, player.y)
        
        # Execute the move
        player.x, player.y = self.destination
        return {"status": "moved", "new_position": self.destination}
    
    def undo(self):
        if self.previous_position:
            player = get_player(self.player_id)
            player.x, player.y = self.previous_position
    
    def serialize(self):
        return {
            "type": "MovePlayerAction",
            "player_id": self.player_id,
            "destination": self.destination,
            "previous_position": self.previous_position
        }

# Action queue and executor
class ActionQueue:
    def __init__(self):
        self.history: list[Action] = []
        self.redo_stack: list[Action] = []
    
    def execute(self, action: Action):
        result = action.execute()
        self.history.append(action)
        self.redo_stack.clear()  # New action invalidates redo
        return result
    
    def undo(self):
        if self.history:
            action = self.history.pop()
            action.undo()
            self.redo_stack.append(action)
    
    def redo(self):
        if self.redo_stack:
            action = self.redo_stack.pop()
            action.execute()
            self.history.append(action)
```

The pattern scales to complex scenarios by allowing actions to contain child actions, enabling hierarchical undo (undoing a "PasteSequence" can undo each individual "PasteItem"), or by implementing the composite pattern for action sequences.

## Practical Applications

Action objects appear in many real-world systems:

- **Game engines**: Player inputs, AI decisions, and engine commands are all modeled as actions with execution, validation, and networking serialization logic
- **IDE and text editors**: Each edit (typing, deletion, formatting) is an action enabling unlimited undo/redo and collaborative editing through action replay
- **Robotic process automation**: Business processes automated by software robots are modeled as sequences of action objects that can be logged, paused, and retried
- **Database migrations**: Upgrades and rollbacks are reversible actions ensuring safe schema evolution

## Examples

Command pattern for a drawing application with macro recording:

```python
class DrawingApp:
    def __init__(self):
        self.canvas = []
        self.undo_stack = []
        self.macro_recording = []
        self.is_recording = False
    
    def execute(self, action):
        result = action.execute()
        self.undo_stack.append(action)
        
        if self.is_recording:
            self.macro_recording.append(action)
        
        return result
    
    def start_recording(self):
        self.is_recording = True
        self.macro_recording = []
    
    def stop_recording(self) -> 'MacroAction':
        self.is_recording = False
        macro = CompositeAction(self.macro_recording.copy())
        self.macro_recording = []
        return macro

# A recorded macro becomes a single undoable action
class CompositeAction(Action):
    def __init__(self, actions: list[Action]):
        self.actions = actions
    
    def execute(self):
        for action in self.actions:
            action.execute()
    
    def undo(self):
        for action in reversed(self.actions):
            action.undo()
```

## Related Concepts

- [[Design Patterns]] - The broader category of reusable architectural solutions
- [[Command Pattern]] - The Gang of Four name for this pattern
- [[undo-log]] / [[redo-log]] - Related patterns for state reversibility
- [[Game Development]] - Domain where action objects are prevalent
- [[Event Sourcing]] - Architectural pattern related to storing action histories

## Further Reading

- "Design Patterns" by Gamma, Helm, Johnson, Vlissides (Gang of Four) - Original command pattern description
- "Game Programming Patterns" by Robert Nystrom - Chapter on command pattern in game development
- "Architecture Patterns with Python" - Command and action patterns in modern Python applications

## Personal Notes

Action objects shine when you need the flexibility to inspect, defer, or reverse operations. I've used them to build automation tools where users could preview, modify, and schedule complex sequences of changes. The overhead is real — more classes, more objects — but the benefits compound when features like undo, logging, and macros become requirements. One anti-pattern to avoid: making actions too large. If a single action does too much, undo becomes coarse-grained and the pattern loses its composability. Favor small, focused actions that combine into larger behaviors. I also recommend versioning your action interfaces; as systems evolve, older serialized actions may need migration logic to execute correctly on newer systems.
