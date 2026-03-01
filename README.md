# 🤖 Autonomous AI Incident Resolution System

An autonomous self-healing system built with **LangChain**, **Pinecone RAG**, and **MCP (Model Context Protocol)** tools. This system can parse production errors, analyze the codebase, generate patches, validate fixes via tests, and simulate pull request creation.

## 🚀 Overview

The system operates in a closed-loop:
1.  **Ingestion**: Receives a production error report (e.g., stack trace).
2.  **Analysis**: Uses RAG (Pinecone) to retrieve relevant code context and documentation.
3.  **Action**: A LangChain agent uses MCP tools to read the code, apply a patch, and run tests.
4.  **Verification**: If tests pass, it creates a Pull Request; if not, it iterates on the fix.

## 🛠️ Architecture

- **Agent**: `langchain-openai` (GPT-4o) powered agent.
- **RAG**: `Pinecone` vector store with `OpenAIEmbeddings`.
- **Tooling**: Custom MCP server implementation providing codebase mutation and validation capabilities.
- **Automation**: CI/CD style orchestration script.

---

## ⚙️ Setup & Installation

### 1. Clone & Install Dependencies
```bash
git clone <repository-url>
cd SelfHealAI
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=pcsk-...
PINECONE_INDEX_NAME=self-heal-index
```

### 3. Initialize Pinecone Index
Ensure you have a Pinecone index created with **1536 dimensions** (for OpenAI embeddings).

---

## 🏃 Run the System

### Phase 1: Index the Codebase
Index your local files into Pinecone to provide the agent with searchable context:
```bash
python3 rag/index_codebase.py
```

### Phase 2: Run Incident Resolution
Simulate a production incident (e.g., a `ZeroDivisionError`) and watch the agent resolve it:
```bash
python3 scripts/automate_resolution.py
```

## 📂 Project Structure
- `agent/`: LangChain agent logic and prompt configuration.
- `mcp_server/`: Custom MCP tool definitions (read, patch, test, PR).
- `rag/`: Indexing and retrieval logic using Pinecone.
- `scripts/`: End-to-end automation and demo scripts.
- `codebase/`: The application codebase monitored by the system.
