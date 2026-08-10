# agents/memory.py
from mem0 import Memory
 
memory = Memory()   # uses in-memory store by default; configure for persistence later
 
def save_memory(user_id: str, content: str):
    memory.add(content, user_id=user_id)
 
def get_memories(user_id: str) -> list:
    return memory.get_all(user_id=user_id)
