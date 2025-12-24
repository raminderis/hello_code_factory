# test_runner_agent.py

import subprocess
import os

class TestRunnerAgent:
    def __init__(self):
        pass

    def run_tests(self, project_root: str = "generated_project"):
        """
        Runs tests using pytest (or a fallback).
        For Hello World, we just run the file directly.
        """
        try:
            # Try pytest first
            print("trying pytest first")
            result = subprocess.run(
                ["pytest", "-q"],
                cwd=project_root,
                capture_output=True,
                text=True
            )
        except FileNotFoundError:
            print("since pytest failed I am trying test_main.py file now which will fail also")
            # Fallback: run the test file manually
            result = subprocess.run(
                ["python3", "test_main.py"],
                cwd=project_root,
                capture_output=True,
                text=True
            )

        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }