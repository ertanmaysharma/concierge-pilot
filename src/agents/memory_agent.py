# src/agents/memory_agent.py
from .base_agent import BaseAgent

class MemoryAgent(BaseAgent):
    def handle(self, input_data):
        action = input_data.get("action")
        user = input_data.get("user")
        if action == "add_preference" and self.memory:
            entry = self.memory.add(user, input_data.get("text",""), metadata=input_data.get("meta"))
            self.log(f"Stored memory for {user}: {entry}")
            return {"status":"stored", "entry": entry}
        elif action == "query" and self.memory:
            hits = self.memory.query(user, k=input_data.get("k",5))
            return {"hits": hits}
        return {"error":"unknown action"}
