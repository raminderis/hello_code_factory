# intent_agent.py

class IntentAgent:
    def __init__(self):
        pass

    def parse(self, user_input: str) -> dict:
        """
        Minimal intent parser for Hello World.
        Later this will call Claude, but for now it's deterministic.
        """
        return {
            "project_name": "hello_world",
            "language": "python",
            "framework": None,
            "features": [user_input]
        }