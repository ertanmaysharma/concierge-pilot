from .base_agent import BaseAgent

class PlannerAgent(BaseAgent):
    def handle(self, input_data):
        """
        If called with {"goal": "..."} it returns a plan list.
        If called with {"goal": "...", "step": "create_itinerary"} it will create a simple itinerary.
        """
        user_goal = input_data.get("goal", "")
        step_override = input_data.get("step")
        self.log(f"Planning for goal: {user_goal}")

        # If an explicit planner step is requested, handle it
        if step_override == "create_itinerary":
            # create a simple itinerary based on the goal (placeholder)
            itinerary = f"Itinerary for '{user_goal}': Day 1 - travel; Day 2 - activities; Day 3 - return."
            self.log(f"Created itinerary for goal: {user_goal}")
            return {"itinerary": itinerary}

        # Normal plan generation
        plan = []
        if "trip" in user_goal.lower():
            plan = [
                {"step":"find_flights","agent":"BookerAgent"},
                {"step":"find_hotels","agent":"BookerAgent"},
                {"step":"create_itinerary","agent":"PlannerAgent"}
            ]
        elif "meal" in user_goal.lower():
            plan = [
                {"step":"collect_preferences","agent":"MemoryAgent"},
                {"step":"suggest_meals","agent":"ShopperAgent"},
                {"step":"create_shopping_list","agent":"ShopperAgent"},
            ]
        else:
            # default flow: clarify goal
            plan = [{"step":"clarify_goal","agent":"PlannerAgent"}]
        return {"plan":plan, "context":{"goal":user_goal}}
