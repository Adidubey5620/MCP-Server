from typing import Literal
from uuid import uuid4

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse
from mcp_server.database import (
    get_all_tasks,
    save_task,
    update_task_status_in_db
)

mcp = FastMCP("MCP Server ACL")

tasks = []

@mcp.tool(name="create_task",description="This tool is created to create new tasks")
def create_task(title:str, priority:str="medium", description:str="") -> dict:
    """
    This function is created to be used as a tool in our server. it creates
    the new todo task to be done later
    """
    task_id = str(uuid4())
    status = "todo"

    task =  {"task_id":task_id, "title":title, "description":description, "status": status, "priority": priority}
    tasks.append(task)
    save_task(task)

    return task

@mcp.tool(name="list_tasks", description="this tool provide all the list of tasks that exists in our database")
def list_tasks() -> list[dict]:
    """
    This function return all the tasks present in our database
    """
    return get_all_tasks() 

@mcp.tool(name="update_task_status", description="This tool will update a specific task status based on its ID")
def update_task_status(task_id:str, status:Literal["todo", "in_progress", "done"]) -> dict:
    """
    this function will update the status of a specific task based on its ID
    """
    return update_task_status_in_db(task_id, status)


app = mcp.http_app()

async def tasks_endpoint(request: Request):
    return JSONResponse(get_all_tasks())

app.add_route("/tasks", tasks_endpoint, methods=["GET"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)