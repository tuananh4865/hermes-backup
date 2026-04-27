#!/usr/bin/env python3
"""
knowledge_graph.py

Knowledge graph storage and traversal using SQLite.
Stores entities and typed relationships.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Optional


class KnowledgeGraph:
    """Knowledge graph with entities and typed relationships."""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = Path.home() / ".hermes" / "knowledge_graph.db"
        else:
            db_path = Path(db_path)
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(db_path))
        self._create_schema()
        
    def _create_schema(self):
        """Create database schema."""
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS entities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity_type TEXT NOT NULL,
                name TEXT NOT NULL,
                attributes TEXT,  -- JSON
                confidence REAL DEFAULT 0.5,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(entity_type, name)
            );
            
            CREATE TABLE IF NOT EXISTS relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_entity TEXT NOT NULL,
                relationship_type TEXT NOT NULL,
                to_entity TEXT NOT NULL,
                attributes TEXT,  -- JSON
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(from_entity, relationship_type, to_entity)
            );
            
            CREATE TABLE IF NOT EXISTS claims (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity_id INTEGER,
                claim_text TEXT NOT NULL,
                source TEXT,
                confidence REAL DEFAULT 0.5,
                status TEXT DEFAULT 'active',  -- active, superseded, stale
                superseded_by INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (entity_id) REFERENCES entities(id),
                FOREIGN KEY (superseded_by) REFERENCES claims(id)
            );
            
            CREATE INDEX IF NOT EXISTS idx_entities_type ON entities(entity_type);
            CREATE INDEX IF NOT EXISTS idx_entities_name ON entities(name);
            CREATE INDEX IF NOT EXISTS idx_relationships_from ON relationships(from_entity);
            CREATE INDEX IF NOT EXISTS idx_relationships_type ON relationships(relationship_type);
            CREATE INDEX IF NOT EXISTS idx_relationships_to ON relationships(to_entity);
            CREATE INDEX IF NOT EXISTS idx_claims_entity ON claims(entity_id);
        """)
        self.conn.commit()
        
    def add_entity(self, entity_type: str, name: str, attributes: dict = None, 
                   confidence: float = 0.5) -> int:
        """Add or update an entity."""
        attributes_json = json.dumps(attributes) if attributes else "{}"
        cursor = self.conn.execute("""
            INSERT INTO entities (entity_type, name, attributes, confidence)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(entity_type, name) DO UPDATE SET
                attributes = excluded.attributes,
                confidence = excluded.confidence,
                updated_at = CURRENT_TIMESTAMP
        """, (entity_type, name, attributes_json, confidence))
        self.conn.commit()
        return cursor.lastrowid
        
    def add_relationship(self, from_entity: str, relationship_type: str, 
                         to_entity: str, attributes: dict = None) -> int:
        """Add or update a relationship."""
        attributes_json = json.dumps(attributes) if attributes else "{}"
        cursor = self.conn.execute("""
            INSERT INTO relationships (from_entity, relationship_type, to_entity, attributes)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(from_entity, relationship_type, to_entity) DO UPDATE SET
                attributes = excluded.attributes
        """, (from_entity, relationship_type, to_entity, attributes_json))
        self.conn.commit()
        return cursor.lastrowid
        
    def add_claim(self, entity_id: int, claim_text: str, source: str = None,
                  confidence: float = 0.5) -> int:
        """Add a claim to an entity."""
        cursor = self.conn.execute("""
            INSERT INTO claims (entity_id, claim_text, source, confidence)
            VALUES (?, ?, ?, ?)
        """, (entity_id, claim_text, source, confidence))
        self.conn.commit()
        return cursor.lastrowid
        
    def supersede_claim(self, claim_id: int, new_claim_id: int):
        """Mark a claim as superseded by a newer claim."""
        self.conn.execute("""
            UPDATE claims SET 
                status = 'superseded',
                superseded_by = ?
            WHERE id = ?
        """, (new_claim_id, claim_id))
        self.conn.commit()
        
    def query(self, start_entity: str, relationship_type: str = None, 
              depth: int = 1) -> list:
        """
        Traverse the graph from a starting entity.
        
        Args:
            start_entity: Entity name to start from
            relationship_type: Optional filter for relationship type
            depth: Traversal depth (1 = direct connections only)
        """
        if relationship_type:
            cursor = self.conn.execute("""
                SELECT from_entity, relationship_type, to_entity, r.attributes
                FROM relationships r
                WHERE from_entity = ? AND relationship_type = ?
            """, (start_entity, relationship_type))
        else:
            cursor = self.conn.execute("""
                SELECT from_entity, relationship_type, to_entity, r.attributes
                FROM relationships r
                WHERE from_entity = ?
            """, (start_entity,))
            
        return cursor.fetchall()
        
    def find_related(self, entity_name: str, relationship_type: str = None) -> list:
        """Find all entities related to this entity."""
        results = []
        
        # Outgoing relationships
        if relationship_type:
            cursor = self.conn.execute("""
                SELECT 'outgoing', relationship_type, to_entity, attributes
                FROM relationships
                WHERE from_entity = ? AND relationship_type = ?
            """, (entity_name, relationship_type))
        else:
            cursor = self.conn.execute("""
                SELECT 'outgoing', relationship_type, to_entity, attributes
                FROM relationships
                WHERE from_entity = ?
            """, (entity_name,))
            
        results.extend([("outgoing",) + row[1:] for row in cursor.fetchall()])
        
        # Incoming relationships
        if relationship_type:
            cursor = self.conn.execute("""
                SELECT 'incoming', relationship_type, from_entity, attributes
                FROM relationships
                WHERE to_entity = ? AND relationship_type = ?
            """, (entity_name, relationship_type))
        else:
            cursor = self.conn.execute("""
                SELECT 'incoming', relationship_type, from_entity, attributes
                FROM relationships
                WHERE to_entity = ?
            """, (entity_name,))
            
        results.extend([("incoming",) + row[1:] for row in cursor.fetchall()])
        
        return results
        
    def get_entity(self, entity_type: str, name: str) -> dict:
        """Get an entity by type and name."""
        cursor = self.conn.execute("""
            SELECT id, entity_type, name, attributes, confidence, created_at, updated_at
            FROM entities
            WHERE entity_type = ? AND name = ?
        """, (entity_type, name))
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "entity_type": row[1],
                "name": row[2],
                "attributes": json.loads(row[3]) if row[3] else {},
                "confidence": row[4],
                "created_at": row[5],
                "updated_at": row[6]
            }
        return None
        
    def get_all_entities(self, entity_type: str = None) -> list:
        """Get all entities, optionally filtered by type."""
        if entity_type:
            cursor = self.conn.execute("""
                SELECT id, entity_type, name, attributes, confidence
                FROM entities
                WHERE entity_type = ?
                ORDER BY name
            """, (entity_type,))
        else:
            cursor = self.conn.execute("""
                SELECT id, entity_type, name, attributes, confidence
                FROM entities
                ORDER BY entity_type, name
            """)
            
        return [
            {
                "id": row[0],
                "entity_type": row[1],
                "name": row[2],
                "attributes": json.loads(row[3]) if row[3] else {},
                "confidence": row[4]
            }
            for row in cursor.fetchall()
        ]
        
    def get_stats(self) -> dict:
        """Get graph statistics."""
        cursor = self.conn.execute("""
            SELECT 
                (SELECT COUNT(*) FROM entities) as entity_count,
                (SELECT COUNT(*) FROM relationships) as relationship_count,
                (SELECT COUNT(*) FROM claims) as claim_count,
                (SELECT COUNT(*) FROM entities GROUP BY entity_type) as by_type
        """)
        row = cursor.fetchone()
        
        type_cursor = self.conn.execute("""
            SELECT entity_type, COUNT(*) FROM entities GROUP BY entity_type
        """)
        by_type = {row[0]: row[1] for row in type_cursor.fetchall()}
        
        return {
            "entity_count": row[0],
            "relationship_count": row[1],
            "claim_count": row[2],
            "entities_by_type": by_type
        }
        
    def close(self):
        """Close database connection."""
        self.conn.close()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Knowledge graph tool")
    parser.add_argument("--init", action="store_true", help="Initialize database")
    parser.add_argument("--stats", action="store_true", help="Show statistics")
    parser.add_argument("--add-entity", nargs=3, metavar=("TYPE", "NAME", "CONFIDENCE"),
                        help="Add entity")
    parser.add_argument("--add-rel", nargs=3, metavar=("FROM", "TYPE", "TO"),
                        help="Add relationship")
    parser.add_argument("--query", help="Query entity")
    parser.add_argument("--db-path", default=None, help="Database path")
    
    args = parser.parse_args()
    
    kg = KnowledgeGraph(args.db_path)
    
    if args.init:
        print("Database initialized")
        
    if args.stats:
        stats = kg.get_stats()
        print(f"Entities: {stats['entity_count']}")
        print(f"Relationships: {stats['relationship_count']}")
        print(f"Claims: {stats['claim_count']}")
        print("By type:")
        for t, c in stats['entities_by_type'].items():
            print(f"  {t}: {c}")
            
    if args.add_entity:
        entity_type, name, confidence = args.add_entity
        kg.add_entity(entity_type, name, confidence=float(confidence))
        print(f"Added entity: [{entity_type}] {name}")
        
    if args.add_rel:
        from_entity, rel_type, to_entity = args.add_rel
        kg.add_relationship(from_entity, rel_type, to_entity)
        print(f"Added relationship: {from_entity} --{rel_type}--> {to_entity}")
        
    if args.query:
        related = kg.find_related(args.query)
        print(f"\nRelated to '{args.query}':")
        for direction, rel_type, target, attrs in related:
            print(f"  [{direction}] {rel_type} -> {target}")
            
    kg.close()


if __name__ == "__main__":
    main()
