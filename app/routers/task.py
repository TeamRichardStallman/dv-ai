from celery.result import AsyncResult
from fastapi import APIRouter

router = APIRouter(prefix="/tasks", tags=["Task"])


@router.get("/{task_id}")
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id)

    if task_result.state == "FAILURE":
        return {
            "task_id": task_id,
            "status": task_result.state,
            "error": task_result.info,
        }

    return {
        "task_id": task_id,
        "status": task_result.state,
        "result": task_result.result if task_result.state == "SUCCESS" else None,
    }
