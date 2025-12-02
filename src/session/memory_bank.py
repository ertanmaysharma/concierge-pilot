# src/session/memory_bank.py
class MemoryBank:
    def __init__(self):
        self.memories = []

    def add(self, user_id, text, metadata=None):
        entry = {"user_id":user_id, "text":text, "meta":metadata}
        self.memories.append(entry)
        return entry

    def query(self, user_id, k=5):
        hits = [m for m in self.memories if m["user_id"]==user_id]
        return hits[-k:]
