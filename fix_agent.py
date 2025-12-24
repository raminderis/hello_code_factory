# fix_agent.py

import os, json
from claude_client import ClaudeClient


class FixAgent:
    """
    Stubbed fix agent.
    In the real system, this will call Claude to fix failing tests.
    """

    def __init__(self):
        self.claude = ClaudeClient()

    def attempt_fix(self, test_results: dict, project_root: str) -> dict:
        """
        Use Claude to fix failing tests by updating project files.
        """

        if test_results["returncode"] == 0:
            return {"fixed": False, "reason": "tests passed"}

        # 1. Read all project files
        project_files = {}
        for root, _, files in os.walk(project_root):
            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(root, file)
                    with open(path, "r") as f:
                        project_files[file] = f.read()

        # 2. Build prompt for Claude
        prompt = f"""
    The tests failed. Here is the pytest output:

    {test_results["stderr"]}

    Here are the current project files(JSON):

    {json.dumps(project_files, indent=2)}

    Fix the code so that all tests pass.

    Return ONLY valid JSON in this format:

    {{
    "files": {{
        "filename.py": "new file contents"
    }}
    }}
    """

        # Step 1: ask ClaudeClient for actual file contents
        fix_json = self.claude.fix_code(prompt)    
        # 2. Apply fixes
        updated_files = fix_json.get("files", {})
        for filename, new_content in updated_files.items():
            path = os.path.join(project_root, filename)
            with open(path, "w") as f:
                f.write(new_content)

        return {"fixed": True, "updated_files": list(updated_files.keys())}