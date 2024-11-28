from fastapi import APIRouter

router = APIRouter(prefix="/tasks", tags=["Task"])


@router.get("/{task_id}", tags=["Task"])
async def get_task_status(task_id: str):
    from celery.result import AsyncResult

    task_result = AsyncResult(task_id)
    return {"task_id": task_id, "status": task_result.status, "result": task_result.result}
