# src/a2a/protocol.py
def make_message(sender, recipient, type_, payload):
    return {"from":sender, "to":recipient, "type":type_, "payload":payload}
