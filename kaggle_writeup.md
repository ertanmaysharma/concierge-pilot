# ConciergePilot — Kaggle Capstone Writeup

**Track:** Concierge Agents
**Title:** ConciergePilot — Multi-Agent Personal Concierge
**Subtitle:** Personal preferences, long-running booking flows, and multi-agent coordination.

## Problem Statement
Concierge tasks (trip planning, meal planning, shopping) are compositional and require specialized sub-skills.
ConciergePilot uses a group of focused agents to plan, search, book, and remember user preferences across sessions.

## Architecture
See `architecture.png` for a diagram. The system includes:
- Orchestrator: accepts user requests and delegates work.
- PlannerAgent, BookerAgent, ShopperAgent, MemoryAgent: specialized sub-agents.
- Tools: MockMCP (booking/search), WebSearch adapter (placeholder), CodeExec (placeholder).
- Sessions & Memory: InMemorySessionService and MemoryBank (long-term memory).
- Observability: SimpleLogger for logs and traces.

## How the submission satisfies rubric
- Multi-agent system: Planner, Booker, Shopper, Memory agents.
- Tools: custom MockMCP plus wrappers.
- Sessions & Memory: InMemorySessionService + MemoryBank for persistent preferences.
- Long-running flows: BookerAgent demonstrates pause/resume via session state.
- Observability: logging hooks present.
- A2A protocol: simple message schema in `src/a2a/protocol.py`.

## Running the demo
1. Install requirements.
2. Run `python src/main.py` — this will simulate a user request and print the plan and results.

## Files of interest
- `src/orchestrator.py` — main coordinator
- `src/agents/` — agent implementations
- `src/tools/mcp.py` — mock provider
- `src/session/` — session and memory implementation
- `src/observability/logger.py` — logging helpers
- `notebooks/demo.ipynb` — optional interactive demo (placeholder)

