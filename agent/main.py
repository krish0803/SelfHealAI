import os
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import Tool
from mcp_server.server import read_file, run_tests, apply_patch, create_pull_request
from rag.retriever import retriever

def get_agent_executor():
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY is not set.")

    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    tools = [
        Tool(
            name="read_code", 
            func=read_file, 
            description="Reads the content of a file in the codebase. Arg: file_path"
        ),
        Tool(
            name="run_tests", 
            func=lambda x: run_tests(), 
            description="Runs tests in the codebase using pytest. No args."
        ),
        Tool(
            name="apply_patch", 
            func=lambda x: apply_patch(*[s.strip() for s in x.split(",", 1)]), 
            description="Applies a code fix to a file. Args: file_path, new_file_content"
        ),
        Tool(
            name="query_knowledge_base", 
            func=lambda x: retriever.query(x) if retriever else "RAG not initialized.", 
            description="Queries the codebase vector store for incident context and similar issues."
        ),
        Tool(
            name="create_pull_request", 
            func=lambda x: create_pull_request(*[s.strip() for s in x.split(",", 1)]), 
            description="Simulates creating a pull request for the fix. Args: branch_name, pr_title"
        )
    ]

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an AI Incident Resolution Specialist. Your goal is to autonomously resolve production incidents. "
                  "1. Query the knowledge base for context. "
                  "2. Read relevant files. "
                  "3. Analyze and generate a patch. "
                  "4. Apply the patch and run tests. "
                  "5. If tests pass, create a pull request describing your fix. "
                  "Always verify your fix with tests before creating a PR."),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_openai_functions_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

def resolve_incident(error_report: str):
    executor = get_agent_executor()
    return executor.invoke({"input": f"Resolve this production incident: {error_report}"})

if __name__ == "__main__":
    # Test call if run directly
    import sys
    if len(sys.argv) > 1:
        print(resolve_incident(sys.argv[1]))
