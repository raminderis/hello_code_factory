from intent_agent import IntentAgent
from planning_agent import PlanningAgent
from codegen_agent import CodegenAgent
from test_runner_agent import TestRunnerAgent
from fix_agent import FixAgent
from gitops_agent import GitOpsAgent


class Orchestrator:
    def __init__(self):
        print("Hello‑World Software Factory initialized.")
        self.intent_agent = IntentAgent()
        self.planning_agent = PlanningAgent()
        self.codegen_agent = CodegenAgent()
        self.test_runner = TestRunnerAgent()
        self.fix_agent = FixAgent()
        self.gitops_agent = GitOpsAgent()

    def run(self, user_input: str):
        print(f"Received request: {user_input}")

        # Step 2: Intent Agent
        spec = self.intent_agent.parse(user_input)
        print("Intent Agent Output:", spec)

        # Step 3: Planning Agent
        plan = self.planning_agent.create_plan(spec)
        print("Planning Agent Output:", plan)

        print("Step 3 complete: Planning Agent is working.")

        # Step 4: Codegen Agent
        result = self.codegen_agent.write_files(plan)
        project_root = result["project_root"]
        print("Codegen Agent Output:", result)

        print("Step 4 complete: Codegen Agent wrote files.")

        # Step 5: Test Runner Agent
        test_results = self.test_runner.run_tests(result["project_root"])
        
        print("Test Runner Output:", test_results)
        print("Step 5 complete: Test Runner is working.")   
        # Fix Loop (stub)
        MAX_FIX_ATTEMPTS = 5
        attempt = 0
        print(f"return code is {test_results["returncode"]}")
        if test_results["returncode"] != 5:
            while test_results["returncode"] != 0 and attempt < MAX_FIX_ATTEMPTS:
                print(f"Fix attempt {attempt + 1}")

                fix_result = self.fix_agent.attempt_fix(test_results, project_root)
                print("Fix Attempt:", fix_result)

                # Re-run tests
                test_results = self.test_runner.run_tests(project_root)
                print("Post-Fix Test Results:", test_results)

                attempt += 1

        if (test_results["returncode"] == 0 or test_results["returncode"] == 5):
            print("All tests passed!")
        else:
            print("Tests still failing after max attempts.")
            print("Exiting.....")
            exit(1)

        # GitOps: init + commit
        init_result = self.gitops_agent.init_repo(project_root)
        print("Git Init:", init_result)

        remote_url = "https://github.com/raminderis/hello_factory.git"
        remote_result = self.gitops_agent.set_remote(project_root, remote_url)
        print("Git Remote:", remote_result)

        commit_result = self.gitops_agent.commit_all(project_root, "AI: initial commit")
        print("Git Commit:", commit_result)

        # # Optional push (stub)
        # push_result = self.gitops_agent.push_stub(project_root)
        # print("Git STUB Push:", push_result)

        # Real push
        push_result = self.gitops_agent.push(project_root)
        print("Git REAL Push:", push_result)

        print("Pipeline complete.")

if __name__ == "__main__":
    orch = Orchestrator()
    orch.run("Create an app which takes two integers and returns the difference between them.")