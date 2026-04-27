#!/usr/bin/env python3
"""
entity_extractor.py

Extracts structured entities from raw sources using LLM.
Entities: Person, Project, Library, Concept, File, Decision
"""

import json
import re
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Entity:
    """Base entity class."""
    entity_type: str
    name: str
    attributes: dict
    relationships: list  # [(relationship_type, target_name)]
    confidence: float = 0.7
    source: str = ""
    
    def to_dict(self):
        return asdict(self)


class EntityExtractor:
    """Extract structured entities from text using heuristics + LLM."""
    
    ENTITY_TYPES = ["Person", "Project", "Library", "Concept", "File", "Decision"]
    
    def __init__(self):
        self.entities = []
        
    def extract(self, text: str, source: str = "") -> list[dict]:
        """
        Extract entities from text.
        Returns list of entity dictionaries.
        """
        # This is a stub - real implementation would use LLM
        # For now, use heuristics for common patterns
        
        entities = []
        
        # Extract Person patterns (name followed by role indicators)
        person_patterns = [
            r'([A-Z][a-z]+ [A-Z][a-z]+)\s+(?:is|was|as)\s+(?:the|a|an)\s+(\w+)',
            r'([A-Z][a-z]+ [A-Z][a-z]+)\s+-\s+(.+)',
        ]
        
        for pattern in person_patterns:
            for match in re.finditer(pattern, text):
                name = match.group(1)
                role = match.group(2) if match.lastindex >= 2 else "unknown"
                entities.append(Entity(
                    entity_type="Person",
                    name=name,
                    attributes={"role": role},
                    relationships=[],
                    source=source
                ))
                
        # Extract Project patterns (quoted names or known project patterns)
        project_patterns = [
            r'(?:project|called|named)\s+["\']?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)["\']?',
            r'(?:building|working on|develo ping)\s+["\']?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)["\']?',
        ]
        
        for pattern in project_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                name = match.group(1)
                entities.append(Entity(
                    entity_type="Project",
                    name=name,
                    attributes={},
                    relationships=[],
                    source=source
                ))
                
        # Extract Library/Framework patterns
        library_patterns = [
            r'\b(React|Vue|Angular|Node\.js|Express|Django|Flask|Rails|Laravel)\b',
            r'\b(Python|JavaScript|TypeScript|Java|C\+\+|Go|Rust)\b',
        ]
        
        for pattern in library_patterns:
            for match in re.finditer(pattern, text):
                name = match.group(1)
                # Avoid duplicates
                if not any(e.name == name for e in entities):
                    entities.append(Entity(
                        entity_type="Library",
                        name=name,
                        attributes={},
                        relationships=[],
                        source=source
                    ))
                    
        # Extract File paths
        file_patterns = [
            r'(?:/|src/|lib/|bin/)([\w/]+\.[a-z]+)',
            r'`([^`]*\.[a-z]+)`',
        ]
        
        for pattern in file_patterns:
            for match in re.finditer(pattern, text):
                path = match.group(1)
                entities.append(Entity(
                    entity_type="File",
                    name=path,
                    attributes={"type": path.split('.')[-1] if '.' in path else "unknown"},
                    relationships=[],
                    source=source
                ))
                
        self.entities.extend(entities)
        return [e.to_dict() for e in entities]
        
    def extract_with_llm(self, text: str, source: str = "", model: str = None) -> list[dict]:
        """
        Extract entities using LLM.
        Requires Hermes Agent or external LLM call.
        
        This is the preferred method for production use.
        """
        # This would call Hermes Agent or external LLM
        # For now, return heuristic extraction
        return self.extract(text, source)
        
    def get_entities(self) -> list[Entity]:
        """Get all extracted entities."""
        return self.entities
        
    def clear(self):
        """Clear all extracted entities."""
        self.entities = []


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Entity extractor")
    parser.add_argument("text", help="Text to extract from")
    parser.add_argument("--source", help="Source document", default="")
    parser.add_argument("--output", help="Output JSON file", default="")
    
    args = parser.parse_args()
    
    extractor = EntityExtractor()
    entities = extractor.extract(args.text, args.source)
    
    print(f"Extracted {len(entities)} entities:")
    for e in entities:
        print(f"  - [{e['entity_type']}] {e['name']}")
        
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(entities, f, indent=2)
        print(f"Written to {args.output}")


if __name__ == "__main__":
    main()
