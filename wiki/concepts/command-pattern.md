---
title: "Command Pattern"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [design-patterns, behavioral-patterns, software-architecture, object-oriented, undo-redo, decoupling]
---

# Command Pattern

## Overview

The Command Pattern is a behavioral design pattern that encapsulates a request as an object, allowing you to parameterize clients with different requests, queue or log requests, and support undoable operations. By turning requests into first-class objects, you gain flexibility in how requests are handled, stored, and manipulated after their creation.

The pattern separates the object that invokes an operation from the object that knows how to perform it. This decoupling means the invoker doesn't need to know anything about the receiver, the action to perform, or how the action is implemented. It simply holds a command object and calls its `execute()` method when appropriate.

This abstraction enables powerful capabilities. Because commands are objects, they can be stored in lists for undo/redo functionality, queued for asynchronous execution, logged for audit trails, or composed into macro commands that execute multiple actions atomically. The command pattern is foundational to many UI frameworks and transaction processing systems.

## Key Concepts

**Command** is the core interface of the pattern. It declares a single method, typically `execute()`, that encapsulates the action to be performed. The interface may also include `undo()` for reversible commands or `redo()` for re-executing undone commands.

**ConcreteCommand** implements the Command interface and defines the binding between a receiver and an action. It holds a reference to the receiver object and stores any parameters needed to execute the action. When executed, the concrete command invokes the appropriate methods on the receiver.

**Receiver** is the object that knows how to perform the actual work associated with the command. Commands delegate to receivers—they don't implement business logic themselves but rather call methods on receivers that do. A receiver might be a document, a database connection, or any object that can perform useful work.

**Invoker** is the object that triggers the command. It holds a reference to a command and calls `execute()` when the request should be processed. The invoker doesn't know anything about the concrete command class or the receiver—it only knows about the Command interface.

**Client** creates ConcreteCommand objects and establishes the binding between commands and their receivers. The client determines which commands are created and which invokers receive them.

## How It Works

The Command Pattern operates through four interconnected roles:

1. **Creation**: The client creates a ConcreteCommand and specifies which receiver will handle the request. The command object stores this relationship.

2. **Invocation**: The invoker holds a command (received from the client or configured elsewhere) and at the appropriate time calls `execute()`.

3. **Execution**: The command's `execute()` method invokes the necessary actions on the receiver. The receiver performs the actual work.

4. **Reversal** (for undoable commands): If the command supports undo, the invoker can call `undo()` which reverses the operation by calling complementary methods on the receiver.

This separation means:
- Commands can be stored in history lists for undo/redo
- Commands can be queued for deferred or asynchronous execution
- Commands can be logged for debugging or audit
- Commands can be composed into complex transactions
- The invoker is completely independent of the business logic

## Practical Applications

The Command Pattern appears throughout software systems:

**Undo/Redo Systems** - Text editors, graphics programs, and IDEs use commands for every user action. The edit history is stored as a list of command objects, allowing users to step backward and forward through their actions.

**GUI Buttons and Menu Items** - GUI frameworks typically map buttons to command objects. The button doesn't know what action it triggers—it just holds a command and calls execute when clicked.

**Macro Recording** - Recording user actions as commands allows playback later. Each action becomes a command object that can be replayed identically.

**Transactional Operations** - Database transactions and financial operations often use commands to bundle multiple actions into atomic units that can be committed or rolled back.

**Task Queues** - Background job systems use commands to represent units of work that can be queued, scheduled, and executed by workers.

**Remote Procedure Call (RPC)** - Commands can be serialized and sent over networks, enabling deferred or distributed execution.

## Examples

```python
from abc import ABC, abstractmethod
from typing import Any

# Command interface
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass

# Receiver
class TextEditor:
    def __init__(self):
        self._content = ""
    
    def insert_text(self, position: int, text: str):
        self._content = self._content[:position] + text + self._content[position:]
    
    def delete_text(self, position: int, length: int):
        deleted = self._content[position:position + length]
        self._content = self._content[:position] + self._content[position + length:]
        return deleted
    
    def get_content(self) -> str:
        return self._content

# Concrete commands
class InsertCommand(Command):
    def __init__(self, editor: TextEditor, position: int, text: str):
        self._editor = editor
        self._position = position
        self._text = text
    
    def execute(self):
        self._editor.insert_text(self._position, self._text)
    
    def undo(self):
        self._editor.delete_text(self._position, len(self._text))

class DeleteCommand(Command):
    def __init__(self, editor: TextEditor, position: int, length: int):
        self._editor = editor
        self._position = position
        self._length = length
        self._deleted_text = ""
    
    def execute(self):
        self._deleted_text = self._editor.delete_text(self._position, self._length)
    
    def undo(self):
        self._editor.insert_text(self._position, self._deleted_text)

# Invoker with history
class CommandManager:
    def __init__(self):
        self._history: list[Command] = []
        self._redo_stack: list[Command] = []
    
    def execute_command(self, command: Command):
        command.execute()
        self._history.append(command)
        self._redo_stack.clear()  # Clear redo stack on new command
    
    def undo(self):
        if not self._history:
            print("Nothing to undo")
            return
        command = self._history.pop()
        command.undo()
        self._redo_stack.append(command)
        print(f"Undid: {command.__class__.__name__}")
    
    def redo(self):
        if not self._redo_stack:
            print("Nothing to redo")
            return
        command = self._redo_stack.pop()
        command.execute()
        self._history.append(command)
        print(f"Redid: {command.__class__.__name__}")

# Usage
editor = TextEditor()
manager = CommandManager()

print(f"Initial content: '{editor.get_content()}'")

manager.execute_command(InsertCommand(editor, 0, "Hello"))
print(f"After insert: '{editor.get_content()}'")

manager.execute_command(InsertCommand(editor, 5, " World"))
print(f"After insert: '{editor.get_content()}'")

manager.execute_command(DeleteCommand(editor, 5, 1))
print(f"After delete: '{editor.get_content()}'")

print("\n--- Undo Stack ---")
manager.undo()
print(f"After undo: '{editor.get_content()}'")

manager.undo()
print(f"After undo: '{editor.get_content()}'")

print("\n--- Redo Stack ---")
manager.redo()
print(f"After redo: '{editor.get_content()}'")
```

## Related Concepts

- [[Design Patterns]] - The broader category of reusable software solutions
- [[Memento Pattern]] - Often paired with command for undo; memento captures state, command changes it
- [[Composite Pattern]] - Composite commands can execute multiple commands as one
- [[Strategy Pattern]] - Similar in that both encapsulate behavior, but strategy selects algorithm while command encapsulates request
- [[Observer Pattern]] - Commands can trigger observer notifications after execution

## Further Reading

- Gamma, Erich, et al. "Design Patterns: Elements of Reusable Object-Oriented Software" (GoF)
- "Head First Design Patterns" by Freeman & Robson
- Qt Framework's command pattern documentation

## Personal Notes

Commands clicked when I started thinking of them as "actions as objects." Every time the user does something in a UI, that action should be a command object. This makes undo trivial, testing straightforward (just call execute on the command), and logging automatic. The key insight is that the command object should be self-contained—it knows the receiver, the action, and enough context to undo itself. I've found that commands work best when they're immutable after creation; mutable commands with internal state get bugs.
