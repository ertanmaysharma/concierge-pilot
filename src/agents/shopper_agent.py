# src/agents/shopper_agent.py
from .base_agent import BaseAgent

class ShopperAgent(BaseAgent):
    def handle(self, input_data):
        step = input_data.get("step")
        user = input_data.get("user", "anonymous")
        self.log(f"Shopper handling {step} for {user}")
        mcp = self.tools.get("mcp")
        if step == "suggest_meals" and self.memory:
            # naive memory retrieval
            prefs = self.memory.query(user, k=5)
            self.log(f"Retrieved preferences: {prefs}")
            # mock suggestion
            suggestions = ["Pasta with tomato sauce", "Grilled chicken salad"] + [p['text'] for p in prefs]
            return {"suggestions": suggestions}
        elif mcp:
            res = mcp.search(step)
            return {"results": res}
        return {"detail": "no-op"}
