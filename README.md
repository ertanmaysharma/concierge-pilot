# ConciergePilot

ConciergePilot is a multi-agent personal concierge implementing planner, booker, shopper and memory agents.
It demonstrates multi-agent coordination, tools, sessions & memory, long-running flows, and observability.

## Quick start (local)

1. Create virtualenv and install:
```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

2. Run demo:
```bash
python src/main.py
```

## Project layout

See `kaggle_writeup.md` for the pitch and architecture. The `src/` folder contains the agent skeletons and tools.

## Notes
- No API keys are included. Use environment variables for production credentials and DO NOT commit them.
- The MockMCP tool simulates provider interactions for safe local demo/testing.
