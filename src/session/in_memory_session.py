# src/session/in_memory_session.py
import threading
class InMemorySessionService:
    def __init__(self):
        self.lock = threading.Lock()
        self.store = {}

    def save(self, key, data):
        with self.lock:
            self.store[key] = data

    def read(self, key):
        with self.lock:
            return self.store.get(key)

    def delete(self, key):
        with self.lock:
            if key in self.store:
                del self.store[key]
