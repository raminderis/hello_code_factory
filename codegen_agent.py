# codegen_agent.py

import os
from claude_client import ClaudeClient

class CodegenAgent:
    def __init__(self):
        self.claude = ClaudeClient()

    def write_files(self, plan: dict, spec: dict | None = None, project_root: str = "generated_project"):
        """
        Uses ClaudeClient to generate file contents from the plan,
        then writes them to disk.
        """
        os.makedirs(project_root, exist_ok=True)

        # Step 1: ask ClaudeClient for actual file contents
        code_response = self.claude.generate_code(plan, spec)
        files = code_response.get("files", {})

        # Step 2: write files to disk
        for filename, content in files.items():
            file_path = os.path.join(project_root, filename)
            with open(file_path, "w") as f:
                f.write(content)

        return {"status": "success", "project_root": project_root, "files": list(files.keys())}