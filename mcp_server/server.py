import os
import subprocess
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("IncidentResolutionServer")

@mcp.tool()
def read_file(file_path: str) -> str:
    """Reads the content of a file in the codebase."""
    abs_path = os.path.abspath(os.path.join("codebase", file_path))
    if not abs_path.startswith(os.path.abspath("codebase")):
        return "Error: Path outside of codebase directory."
    try:
        with open(abs_path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

@mcp.tool()
def run_tests() -> str:
    """Runs tests in the codebase using pytest."""
    try:
        result = subprocess.run(["pytest", "codebase"], capture_output=True, text=True)
        return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}\nReturn Code: {result.returncode}"
    except Exception as e:
        return f"Error running tests: {str(e)}"

@mcp.tool()
def apply_patch(file_path: str, patch_content: str) -> str:
    """Applies a patch to a file in the codebase."""
    abs_path = os.path.abspath(os.path.join("codebase", file_path))
    if not abs_path.startswith(os.path.abspath("codebase")):
        return "Error: Path outside of codebase directory."
    try:
        with open(abs_path, "w") as f:
            f.write(patch_content)
        return f"Successfully applied patch to {file_path}"
    except Exception as e:
        return f"Error applying patch: {str(e)}"

@mcp.tool()
def create_pull_request(branch_name: str, title: str) -> str:
    """Simulates creating a pull request."""
    return f"PR created: {title} on branch {branch_name} (Simulated)"

if __name__ == "__main__":
    mcp.run()
