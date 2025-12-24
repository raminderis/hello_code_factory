# gitops_agent.py

import os
import subprocess

class GitOpsAgent:
    """
    Minimal GitOps agent for local commits.
    Later this can push to GitHub/GitLab.
    """

    def __init__(self):
        self.github_user = os.getenv("GITHUB_USER")
        self.github_token = os.getenv("GITHUB_TOKEN")

    def init_repo(self, project_root: str):
        """
        Initialize a git repo if it doesn't exist.
        """
        if not os.path.exists(os.path.join(project_root, ".git")):
            subprocess.run(["git", "init"], cwd=project_root)
            return {"initialized": True}
        print(f"project root : {project_root}")
        print(os.path.exists(os.path.join(project_root, ".git")))
        return {"initialized": False}

    def set_remote(self, project_root: str, remote_url: str):
        """
        Ensure the Git remote 'origin' is set to the given URL.
        If a remote already exists, update it.
        If no remote exists, add it.
        """

        # Check if a remote already exists
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=project_root,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            # Remote exists → update it
            subprocess.run(
                ["git", "remote", "set-url", "origin", remote_url],
                cwd=project_root
            )
            return {
                "remote_set": True,
                "action": "updated",
                "remote_url": remote_url
            }

        # No remote exists → add it
        subprocess.run(
            ["git", "remote", "add", "origin", remote_url],
            cwd=project_root
        )
        return {
            "remote_set": True,
            "action": "added",
            "remote_url": remote_url
        }

    def commit_all(self, project_root: str, message: str = "AI: initial commit"):
        """
        Stage all files and commit.
        """
        subprocess.run(["git", "add", "."], cwd=project_root)
        result = subprocess.run(
            ["git", "commit", "-m", message],
            cwd=project_root,
            capture_output=True,
            text=True
        )

        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    def push_stub(self, project_root: str):
        """
        Stubbed push — prints instead of pushing.
        """
        return {"pushed": False, "reason": "push stubbed out"}
    

    def push(self, project_root: str, branch: str = "main"):
        if not self.github_user or not self.github_token:
            return {"pushed": False, "reason": "Missing GITHUB_USER or GITHUB_TOKEN"}

        # Get remote URL
        remote_url = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=project_root,
            capture_output=True,
            text=True
        ).stdout.strip()

        # Inject token temporarily
        authed_url = remote_url.replace(
            "https://",
            f"https://{self.github_user}:{self.github_token}@"
        )

        subprocess.run(["git", "remote", "set-url", "origin", authed_url], cwd=project_root)

        # Ensure branch exists locally
        subprocess.run(["git", "checkout", "-B", branch], cwd=project_root)

        # Real push
        result = subprocess.run(
            ["git", "push", "-u", "origin", branch],
            cwd=project_root,
            capture_output=True,
            text=True
        )

        # Restore clean remote URL
        subprocess.run(["git", "remote", "set-url", "origin", remote_url], cwd=project_root)

        # Fetch to update remote tracking
        subprocess.run(["git", "fetch", "origin"], cwd=project_root)

        return {
            "pushed": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr
        }