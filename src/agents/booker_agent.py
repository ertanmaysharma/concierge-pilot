from .base_agent import BaseAgent
import time

class BookerAgent(BaseAgent):
    def handle(self, input_data):
        """
        Improved booker: if session contains a started step, resume it.
        Simulates a long-running operation by checking and updating session state.
        """
        step = input_data.get("step")
        session_key = input_data.get("session_id", "default-session")
        params = input_data.get("params", {})

        # If session exists and step is started but not completed, report resume behavior.
        existing = None
        if self.session:
            existing = self.session.read(session_key)

        # If existing indicates the same step was started but not completed, resume
        if existing and existing.get("status") == "started" and existing.get("step") == step:
            self.log(f"Resuming booking step '{step}' from session {session_key}")
            # Simulate finishing
            result = self.tools.get("mcp").book(step, params) if self.tools.get("mcp") else {"step": step, "success": False}
            existing.update({"status":"completed", "result": result})
            self.session.save(session_key, existing)
            return {"status": "resumed_and_completed", "result": result}

        # Otherwise start the booking step
        self.log(f"Handling booking step: {step}")
        state = {"status":"started", "step":step, "started_at": time.time(), "params": params}
        if self.session:
            self.session.save(session_key, state)

        # Simulate a call to the MCP tool (mock) and potential delay
        mcp = self.tools.get("mcp")
        if mcp:
            # simulate processing
            result = mcp.book(step, params)
        else:
            result = {"step": step, "success": False, "details":"No MCP tool available"}

        # finalize state
        state.update({"status":"completed", "result": result, "completed_at": time.time()})
        if self.session:
            self.session.save(session_key, state)
        self.log(f"Booking step completed: {step}")
        return {"status":"done", "result": result}
