# src/observability/logger.py
import time, json

class SimpleLogger:
    def log(self, agent, message, **meta):
        ts = time.time()
        rec = {"ts": ts, "agent": agent, "message": message, "meta": meta}
        print(json.dumps(rec))
