import asyncio
from typing import Any, Dict

import pytest
from httpx import AsyncClient


async def retry_task_execution(
    client: AsyncClient, task_id: str, max_retries: int = 3, timeout: int = 60
) -> Dict[str, Any]:
    for retry_count in range(max_retries):
        for _ in range(timeout):
            task_response = await client.get(f"/tasks/{task_id}")
            assert task_response.status_code == 200, f"Task status check failed with status {task_response.status_code}"

            task_status = task_response.json()

            if task_status["status"] == "SUCCESS":
                result = task_status.get("result", {}).get("result")
                if result is not None:
                    return result

                if retry_count < max_retries - 1:
                    print(f"Attempt {retry_count + 1}: Task returned None, retrying...")
                    break
                else:
                    pytest.fail(f"Task returned None after {max_retries} attempts")

            elif task_status["status"] == "FAILURE":
                error_msg = task_status.get("error", "No error message provided")
                pytest.fail(f"Task failed with error: {error_msg}")

            await asyncio.sleep(1)
        else:
            if retry_count < max_retries - 1:
                print(f"Attempt {retry_count + 1}: Task timed out, retrying...")
                continue
            pytest.fail(f"Task did not complete within {timeout} seconds after {max_retries} attempts")

    pytest.fail(f"Task failed after {max_retries} retries")
