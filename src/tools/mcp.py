# src/tools/mcp.py
class MockMCP:
    def __init__(self):
        pass

    def book(self, step, params):
        # deterministic mock response
        return {"step": step, "success": True, "details": f"Mock booking for {step} with {params}"}

    def search(self, query):
        return [{"id": "mock1", "title": f"Result for {query}", "price": 100}]
