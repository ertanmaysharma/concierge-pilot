# src/orchestrator.py
from agents.planner_agent import PlannerAgent
from agents.booker_agent import BookerAgent
from agents.shopper_agent import ShopperAgent
from agents.memory_agent import MemoryAgent
from tools.mcp import MockMCP
from session.in_memory_session import InMemorySessionService
from session.memory_bank import MemoryBank
from observability.logger import SimpleLogger

class Orchestrator:
    def __init__(self):
        self.session = InMemorySessionService()
        self.memory = MemoryBank()
        self.tools = {"mcp": MockMCP()}
        self.logger = SimpleLogger()
        # instantiate agents
        self.planner = PlannerAgent("Planner", self.session, self.memory, self.tools, self.logger)
        self.booker = BookerAgent("Booker", self.session, self.memory, self.tools, self.logger)
        self.shopper = ShopperAgent("Shopper", self.session, self.memory, self.tools, self.logger)
        self.memory_agent = MemoryAgent("Memory", self.session, self.memory, self.tools, self.logger)

    def handle_user(self, user_id, goal):
        plan_resp = self.planner.handle({"goal": goal})
        plan = plan_resp.get("plan", [])
        results = []
        session_id = f"session-{user_id}"
        for step in plan:
            agent_name = step.get("agent")
            step_name = step.get("step")
            if agent_name == "BookerAgent" or agent_name == "BookerAgent".replace("Agent","")+"Agent":
                r = self.booker.handle({"step": step_name, "session_id": session_id, "params": {"user":user_id}})
                results.append(r)
            elif agent_name == "ShopperAgent":
                r = self.shopper.handle({"step": step_name, "user": user_id})
                results.append(r)
            elif agent_name == "MemoryAgent":
                r = self.memory_agent.handle({"action":"query","user":user_id})
                results.append(r)
            else:
                r = {"detail":"noop"}
                results.append(r)
        return {"plan":plan, "results":results, "session_id": session_id}
