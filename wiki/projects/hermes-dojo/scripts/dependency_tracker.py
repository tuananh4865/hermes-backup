#!/usr/bin/env python3
"""
dependency_tracker.py

Maps function call graph to prevent cascade failures.
Run before editing any file.
"""

import ast
import os
import sys
import json
from pathlib import Path
from collections import defaultdict


class DependencyTracker:
    """Track function calls and imports across a codebase."""
    
    def __init__(self, root_path: str):
        self.root = Path(root_path)
        self.call_graph = defaultdict(list)  # function -> [callers]
        self.import_graph = defaultdict(list)  # module -> [importers]
        self.file_functions = defaultdict(list)  # file -> [functions defined]
        
    def scan(self, specific_file: str = None):
        """Scan entire codebase for dependencies."""
        scan_root = Path(specific_file) if specific_file else self.root
        
        # If a specific file was requested, only analyze that file
        if specific_file:
            print(f"Analyzing {specific_file}...")
            try:
                self._analyze_file(Path(specific_file))
                print(f"Scanned 1 file")
            except Exception as e:
                print(f"Warning: Could not analyze {specific_file}: {e}")
            return
            
        # Otherwise scan entire root directory
        print(f"Scanning {self.root}...")
        count = 0
        for py_file in self.root.rglob("*.py"):
            try:
                self._analyze_file(py_file)
                count += 1
            except Exception as e:
                print(f"Warning: Could not analyze {py_file}: {e}")
        print(f"Scanned {count} Python files")
        
    def _analyze_file(self, path: Path):
        """Extract function calls and imports from a file."""
        try:
            content = path.read_text()
            tree = ast.parse(content)
        except Exception:
            return
            
        functions_defined = []
        
        for node in ast.walk(tree):
            # Function definitions
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions_defined.append(node.name)
                
            # Function calls
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    self.call_graph[node.func.id].append(str(path))
                elif isinstance(node.func, ast.Attribute):
                    self.call_graph[node.func.attr].append(str(path))
                    
        # Store functions defined in this file
        for func in functions_defined:
            self.file_functions[str(path)].append(func)
                
        # Imports
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module:
                    self.import_graph[node.module].append(str(path))
                for alias in node.names:
                    self.import_graph[alias.name].append(str(path))
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.import_graph[alias.name].append(str(path))
                    
    def find_callers(self, function_name: str) -> list:
        """Find all files that call a function."""
        return list(set(self.call_graph.get(function_name, [])))
        
    def find_imports(self, module_name: str) -> list:
        """Find all files that import a module."""
        return list(set(self.import_graph.get(module_name, [])))
        
    def find_functions_in_file(self, file_path: str) -> list:
        """Find all functions defined in a file."""
        return self.file_functions.get(file_path, [])
        
    def run_pre_edit_check(self, file_path: str, function_name: str = None):
        """Run dependency check before editing."""
        # Resolve to absolute path for consistent lookup
        file_path = str(Path(file_path).resolve())
        
        print(f"\n{'='*60}")
        print(f"PRE-EDIT DEPENDENCY CHECK")
        print(f"{'='*60}")
        print(f"File: {file_path}")
        
        # Find functions in this file
        funcs = self.find_functions_in_file(file_path)
        print(f"\nFunctions defined in this file: {len(funcs)}")
        for f in funcs[:10]:
            print(f"  - {f}")
            
        if function_name:
            # Check specific function
            callers = self.find_callers(function_name)
            print(f"\nFunction: {function_name}")
            print(f"Callers ({len(callers)}):")
            for c in callers:
                print(f"  - {c}")
        else:
            # Check all functions in file
            print(f"\nChecking all functions in file...")
            for func in funcs:
                callers = self.find_callers(func)
                if callers:
                    print(f"\n  {func} — {len(callers)} callers:")
                    for c in callers[:5]:
                        print(f"    - {c}")
                        
        print(f"\n{'='*60}")
        print("CASCADE PREVENTION CHECKLIST")
        print(f"{'='*60}")
        print("Before editing:")
        print("  [ ] Read ALL callers listed above")
        print("  [ ] List ALL files that need updates")
        print("  [ ] Update base/interface FIRST, then callers")
        print("After editing:")
        print("  [ ] Verify base change complete")
        print("  [ ] Verify EACH caller updated")
        print("  [ ] Run tests for base + callers")
        print(f"{'='*60}\n")
        
    def generate_report(self, output_path: str = None):
        """Generate dependency report."""
        report = {
            "call_graph": {k: list(set(v)) for k, v in self.call_graph.items()},
            "import_graph": {k: list(set(v)) for k, v in self.import_graph.items()},
            "file_functions": dict(self.file_functions)
        }
        
        if output_path:
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"Report written to {output_path}")
            
        return report


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Dependency tracker for cascade prevention")
    parser.add_argument("path", help="Path to scan (file or directory)")
    parser.add_argument("--scan", action="store_true", help="Scan and report")
    parser.add_argument("--check", help="File to check (for caller analysis)")
    parser.add_argument("--function", help="Function to check callers for")
    parser.add_argument("--output", help="Output JSON file")
    
    args = parser.parse_args()
    
    # Always resolve path to absolute for consistent behavior
    root_path = str(Path(args.path).resolve())
    
    tracker = DependencyTracker(root_path)
    
    if args.scan:
        if args.check:
            # When --check is provided, scan ENTIRE codebase to find callers
            tracker.scan()
            # Then run pre-edit check on the specific file
            tracker.run_pre_edit_check(args.check, args.function)
        else:
            # Scan entire root directory
            tracker.scan()
            tracker.run_pre_edit_check(root_path)
        
    if args.output:
        tracker.generate_report(args.output)


if __name__ == "__main__":
    main()
