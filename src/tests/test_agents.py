# src/tests/test_agents.py
from orchestrator import Orchestrator

def test_planner_trip():
    orch = Orchestrator()
    plan = orch.planner.handle({'goal':'Plan a trip'})['plan']
    assert any(s['step']=='find_flights' for s in plan)

def test_end_to_end():
    orch = Orchestrator()
    out = orch.handle_user('u1','Plan a weekend trip')
    assert 'plan' in out and 'results' in out
