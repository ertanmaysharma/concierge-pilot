# src/agents/base_agent.py
import uuid
from typing import Dict, Any

class BaseAgent:
    def __init__(self, name: str, session_service=None, memory=None, tools=None, logger=None):
        self.name = name
        self.id = f"{name}-{uuid.uuid4().hex[:6]}"
        self.session = session_service
        self.memory = memory
        self.tools = tools or {}
        self.logger = logger

    def log(self, msg: str, **meta):
        if self.logger:
            self.logger.log(self.name, msg, **meta)
        else:
            print(f"[{self.name}] {msg}")

    def handle(self, input_data: Dict[str,Any]) -> Dict[str,Any]:
        raise NotImplementedError("Agents implement handle()")
