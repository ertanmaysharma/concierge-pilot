from orchestrator import Orchestrator
import time

def interactive_loop():
    orch = Orchestrator()

    # seed memory with preferences for demo
    orch.memory.add('user123', 'Prefers window seat and vegetarian meals', metadata={'type':'pref'})

    print("Welcome to ConciergePilot demo.")
    print("Type a goal like: 'Plan a weekend trip' or 'Plan my weekly meals' or 'exit' to quit.\n")

    while True:
        user_input = input("What would you like me to plan? ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye.")
            break

        user_id = "user123"
        # run planner to get plan first (so we can optionally display/confirm)
        plan_resp = orch.planner.handle({"goal": user_input})
        plan = plan_resp.get("plan", [])
        print("\nGenerated plan:")
        for i, step in enumerate(plan, start=1):
            print(f"  {i}. {step['step']}  (agent: {step['agent']})")
        confirm = input("\nProceed with executing the plan? (y/n) ").strip().lower()
        if confirm not in ("y", "yes"):
            print("Plan cancelled. You can enter another goal.\n")
            continue

        # run the plan with interactive pause/resume for booking steps
        session_id = f"session-{user_id}-{int(time.time())}"
        print(f"\nStarting execution (session id: {session_id})...\n")
        itinerary = []
        for step in plan:
            agent_name = step.get("agent")
            step_name = step.get("step")

            if agent_name == "BookerAgent":
                # allow pause/resume during bookings
                print(f"[Booker] Executing booking step: {step_name}")
                r = orch.booker.handle({"step": step_name, "session_id": session_id, "params": {"user": user_id}})
                print(" -> Result:", r)
                # After a booking step, ask if user wants to pause the long-running flow
                while True:
                    ans = input("Pause now and save state to resume later? (y/n) ").strip().lower()
                    if ans in ("y", "yes"):
                        print(f"State saved to session '{session_id}'. To resume later, run the 'resume' command in this program.")
                        break
                    elif ans in ("n", "no"):
                        break
                    else:
                        print("Please answer y or n.")
                # continue (we do not actually block the process here)
            elif agent_name == "ShopperAgent":
                print(f"[Shopper] Executing shopper step: {step_name}")
                r = orch.shopper.handle({"step": step_name, "user": user_id})
                print(" -> Result:", r)
            elif agent_name == "PlannerAgent":
                # handle any planner internal steps (e.g., create_itinerary)
                print(f"[Planner] Executing planner step: {step_name}")
                r = orch.planner.handle({"goal": user_input, "step": step_name})
                # if the planner returned an itinerary, capture it
                if isinstance(r, dict) and r.get("itinerary"):
                    itinerary.append(r["itinerary"])
                    print(" -> Itinerary piece:", r["itinerary"])
                else:
                    print(" -> Planner step result:", r)
            elif agent_name == "MemoryAgent":
                print(f"[Memory] Executing memory step: {step_name}")
                r = orch.memory_agent.handle({"action": "query", "user": user_id})
                print(" -> Memory query result:", r)
            else:
                print(f"[{agent_name}] Unknown agent type, skipping step: {step_name}")

        # After plan run, print session state and itinerary
        print("\nExecution completed for this run.")
        state = orch.session.read(session_id)
        print("Final session state (latest):", state)
        if itinerary:
            print("\n=== Final Itinerary ===")
            for part in itinerary:
                print("-", part)
        print("\nIf you saved state and want to resume a booking flow later, type 'resume' now or press Enter to continue.")
        cmd = input("Command (resume / continue / exit): ").strip().lower()
        if cmd == "resume":
            resume_session_flow(orch, session_id, user_id)
        if cmd in ("exit", "quit"):
            print("Goodbye.")
            break
        print("\n--- Ready for the next request ---\n")

def resume_session_flow(orch, session_id, user_id):
    print(f"\nAttempting to resume session {session_id} ...")
    state = orch.session.read(session_id)
    if not state:
        print("No saved state found for that session id.")
        return
    print("Loaded state:", state)
    # In this simple demo, assume any saved 'step' that is not completed can be resumed.
    if state.get("status") == "started":
        print("Resuming the booking step:", state.get("step"))
        r = orch.booker.handle({"step": state.get("step"), "session_id": session_id, "params": {"user": user_id}})
        print("Resume result:", r)
        print("Updated session:", orch.session.read(session_id))
    else:
        print("The saved step appears completed. Nothing to resume.")

if __name__ == '__main__':
    interactive_loop()
