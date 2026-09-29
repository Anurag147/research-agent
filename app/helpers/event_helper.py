import json


def generate_sse_event(event: dict):
    return f"data: {json.dumps(event)}\n\n"
