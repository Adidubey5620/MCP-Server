# MCP Server — Task Manager

A task management server built with [FastMCP](https://github.com/jlowin/fastmcp), exposing tools via the Model Context Protocol (MCP). Includes a LangChain + LangGraph AI agent client that interacts with the server using natural language.

---

## Features

- MCP tools: `create_task`, `list_tasks`, `update_task_status`
- SQLite persistence (`data/tasks.db`)
- REST endpoint: `GET /tasks`
- AI agent client powered by LangChain + LangGraph with conversation memory (checkpoints)

---

## Project Structure

```
MCP server/
├── src/mcp_server/
│   ├── server.py           # FastMCP server & tools
│   ├── database.py         # SQLite CRUD operations
│   ├── client.py           # Raw MCP client (testing)
│   └── langchain_client.py # LangChain AI agent client
├── data/tasks.db           # SQLite database
├── checkpoints.db          # LangGraph conversation memory
├── pyproject.toml
└── .env
```

---

## Setup

**Requirements:** Python 3.12+, [uv](https://github.com/astral-sh/uv)

```bash
uv sync
```

Create a `.env` file:

```env
OPENROUTER_API_KEY=<your_openrouter_api_key>
```

---

## Usage

### Start the server

```bash
uvicorn mcp_server.server:app --host 127.0.0.1 --port 8000
```

### Run the AI agent (interactive chat)

```bash
uv run python src/mcp_server/langchain_client.py
```

### Run the raw MCP client (for testing)

```bash
uv run python src/mcp_server/client.py
```

---

## MCP Tools

| Tool | Description |
|---|---|
| `create_task` | Creates a new task with title, priority, and description |
| `list_tasks` | Returns all tasks from the database |
| `update_task_status` | Updates a task's status (`todo`, `in_progress`, `done`) |

---

## REST API

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/tasks` | Returns all tasks as JSON |
| `*` | `/mcp` | MCP protocol endpoint |
