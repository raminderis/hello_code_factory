# claude_client.py
# claude_client.py

import anthropic
import json
import os, re

class ClaudeClient:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-5"

    def generate_plan(self, spec: dict) -> dict:
        """
        Ask Claude to generate a real project plan.
        """
        prompt = self._build_prompt(spec)
        print(f"plan prompt is {prompt}")
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        print(f"response back from claude : {response}")
        # Claude returns text — you parse JSON out of it
        return self._parse_plan(response.content[0].text)

    def _build_prompt(self, spec: dict) -> str:
        return f"""
            You are a planning agent. Create a file plan for this project.

            Project spec (JSON):
            {spec}

            Return ONLY valid JSON in this format and Do NOT wrap it in code fences. Do NOT add explanations.

            {{
            "files": {{
                "path/to/file.py": "description of file",
                "another/file.py": "description"
            }}
            }}
        """

    def _parse_plan(self, text: str) -> dict:
        # Find the first JSON object in the text
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError("No JSON object found in Claude response")

        json_str = match.group(0)
        print(f"join str is. {json_str}")
        return json.loads(json_str)

    def _extract_json(self, text: str) -> dict:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError("No JSON found in Claude response")
        return json.loads(match.group(0))

    def generate_code(self, plan: dict, spec: dict | None = None) -> dict:
        """
        Ask Claude to generate real file contents for each file in the plan.
        """

        prompt = f"""
You are a code generation agent.

Here is the project plan (JSON):
{plan}

Here is the project spec (JSON):
{spec}

For each file in plan["files"], generate the full file contents.

Return ONLY valid JSON in this format:

{{
"files": {{
    "filename.py": "full file contents here",
    "another_file.py": "full file contents here"
}}
}}
"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract JSON from Claude's response
        return self._extract_json(response.content[0].text)

    def fix_code(self, prompt: str) -> dict:
        """
        Ask Claude to generate real file contents for each file in the prompt.
        """

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract JSON from Claude's response
        return self._extract_json(response.content[0].text)

    # def generate_code(self, plan: dict, spec: dict | None = None) -> dict:
    #     """
    #     Simulate Claude generating actual file contents from a plan.

    #     In the real version, this would:
    #     - read the plan
    #     - consider the spec
    #     - return real code for each file
    #     """
    #     project_name = None
    #     if spec:
    #         project_name = spec.get("project_name")

    #     files = {}

    #     for filename, marker in plan.get("files", {}).items():
    #         if filename == "main.py":
    #             files[filename] = (
    #                 "def main():\n"
    #                 f"    print('Hello from {project_name or 'project'}')\n\n"
    #                 "if __name__ == '__main__':\n"
    #                 "    main()\n"
    #             )
    #         elif filename == "test_main.py":
    #             files[filename] = (
    #                 "def test_placeholder():\n"
    #                 "    assert True\n"
    #             )
    #         else:
    #             # fallback: just echo a stub
    #             files[filename] = f"# Stub for {filename}\n"

    #     return {"files": files}