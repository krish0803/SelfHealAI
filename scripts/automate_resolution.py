import os
import sys

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.main import resolve_incident

def run_production_flow():
    # Simulate a production error report
    # We'll revert the manual fix first to ensure the agent has something to solve
    buggy_code = 'def divide(a, b):\n    return a / b\n'
    with open("codebase/app.py", "w") as f:
        f.write(buggy_code)

    error_report = "Critical Incident: ZeroDivisionError: division by zero in codebase/app.py at line 3"
    
    print("--- Starting Autonomous AI Incident Resolution ---")
    print(f"Error Report: {error_report}\n")

    if not os.getenv("OPENAI_API_KEY"):
        print("CRITICAL: OPENAI_API_KEY not found. Please set it to run the real agent.")
        sys.exit(1)

    try:
        result = resolve_incident(error_report)
        print("\n--- Resolution Completed ---")
        print(f"Agent Final Response: {result['output']}")
    except Exception as e:
        print(f"\n--- Incident Resolution Failed ---\n{str(e)}")

if __name__ == "__main__":
    run_production_flow()
