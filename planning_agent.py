# planning_agent.py

from claude_client import ClaudeClient

class PlanningAgent:
    def __init__(self):
        self.claude = ClaudeClient()

    def create_plan(self, spec: dict) -> dict:
        """
        Planning logic: ask ClaudeClient for a file plan.
        """
        return self.claude.generate_plan(spec)