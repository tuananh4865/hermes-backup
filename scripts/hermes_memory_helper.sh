#!/usr/bin/env bash
# Hermes Holographic Memory Helper
# Use fact_store actions: add, search, probe, list, etc.
#
# Activation: anh cần restart gateway trước:
#   bash ~/.hermes/restart-hermes-gateway.sh
#
# Sau đó em sẽ có fact_store tool trong session.

# Sử dụng:
#   fact_store action=add content="..." category="project" tags="..."
#   fact_store action=search query="..."
#   fact_store action=probe entity="..."
#   fact_store action=list

echo "ℹ️  fact_store tool chỉ available SAU KHI restart gateway"
echo "ℹ️  Em sẽ tự gọi fact_store khi cần add/search memory"
echo ""
echo "📊 Current DB status:"
~/.hermes/hermes-agent/.venv/bin/python -c "
import os
os.environ['HERMES_HOME'] = '/Users/tuananh4865/.hermes'
from plugins.memory.holographic.store import MemoryStore
store = MemoryStore(db_path='/Users/tuananh4865/.hermes/memory_store.db')
print(f'  Facts in holographic DB: {len(store.list_facts())}')
print(f'  DB path: {store.db_path}')
"