import asyncio

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.tests.data.evaluation import EVALUATION_REQUEST_DATA

BASE_URL = "http://test"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "interview_id, interview_mode, interview_type, interview_method, question_count, file_paths",
    [
        (1, "real", "technical", "chat", 1, ["cover-letters/SK_AI_01.txt"]),
        (2, "real", "personal", "chat", 1, ["cover-letters/SK_AI_01.txt"]),
        (3, "real", "technical", "voice", 1, ["cover-letters/cover_letter_01.txt"]),
        (4, "general", "technical", "chat", 1, []),
    ],
)
async def test_create_interview_questions(
    interview_id, interview_mode, interview_type, interview_method, question_count, file_paths
):
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as ac:
        response = await ac.post(
            f"/interview/{interview_id}/questions",
            json={
                "user_id": 1,
                "interview_mode": interview_mode,
                "interview_type": interview_type,
                "interview_method": interview_method,
                "job_role": "ai",
                "question_count": question_count,
                "file_paths": file_paths,
            },
        )

        assert response.status_code == 200
        response_json = response.json()

        assert "task_id" in response_json, "Response must contain task_id"
        task_id = response_json["task_id"]

        for _ in range(60):
            task_response = await ac.get(f"/tasks/{task_id}")
            assert task_response.status_code == 200
            task_status = task_response.json()

            if task_status["status"] == "SUCCESS":
                assert "result" in task_status, "Response must contain 'result'"
                result = task_status["result"]

                assert "result" in result, "result must contain 'result'"
                result = result["result"]

                assert "questions" in result, "Result must contain 'questions'"
                questions = result["questions"]

                assert (
                    len(questions) == question_count
                ), f"Expected {question_count} questions, but got {len(questions)}"
                break
            elif task_status["status"] == "FAILURE":
                pytest.fail(f"Task failed with error: {task_status.get('error')}")
            else:
                await asyncio.sleep(1)
        else:
            pytest.fail("Task did not complete within the allowed time.")


@pytest.mark.asyncio
async def test_create_interview_evaluation():
    evaluation_request_data = EVALUATION_REQUEST_DATA

    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as ac:
        response = await ac.post("/interview/1/evaluation", json=evaluation_request_data)
        assert response.status_code == 200
        response_json = response.json()

        assert "task_id" in response_json, "Response must contain task_id"
        task_id = response_json["task_id"]

        for _ in range(120):
            task_response = await ac.get(f"/tasks/{task_id}")
            assert task_response.status_code == 200
            task_status = task_response.json()

            if task_status["status"] == "SUCCESS":
                assert "result" in task_status, "Response must contain 'result'"
                result = task_status["result"]

                assert "result" in result, "result must contain 'result'"
                result = result["result"]

                assert "overall_evaluation" in result, "Result must contain 'overall_evaluation'"
                overall_evaluation = result["overall_evaluation"]

                assert "text_overall" in overall_evaluation, "Overall evaluation must contain 'text_overall'"
                assert "voice_overall" in overall_evaluation, "Overall evaluation must contain 'voice_overall'"

                break
            elif task_status["status"] == "FAILURE":
                pytest.fail(f"Task failed with error: {task_status.get('error')}")
            else:
                await asyncio.sleep(1)
        else:
            pytest.fail("Task did not complete within the allowed time.")


@pytest.mark.asyncio
@pytest.mark.parametrize("interview_method", ["chat", "voice"])
async def test_create_answer_text_from_answer_audio(interview_method):
    answer_data = {
        "interview_method": interview_method,
        "user_id": 0,
        "answer": {
            "answer_text": "answer test",
            "s3_audio_url": "test/questions/audio_1.mp3",
            "s3_video_url": "string",
        },
    }

    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as ac:
        response = await ac.post("/interview/1/answer/1", json=answer_data)
        assert response.status_code == 200
        response_json = response.json()

        assert "task_id" in response_json, "Response must contain task_id"
        task_id = response_json["task_id"]

        for _ in range(60):
            task_response = await ac.get(f"/tasks/{task_id}")
            assert task_response.status_code == 200
            task_status = task_response.json()

            if task_status["status"] == "SUCCESS":
                assert "result" in task_status, "Response must contain 'result'"
                result = task_status["result"]

                assert "result" in result, "result must contain 'result'"
                result = result["result"]

                assert "answer" in result, "Result must contain 'answer'"
                answer = result["answer"]

                assert "answer_text" in answer, "Answer must contain 'answer_text'"
                if interview_method == "chat":
                    assert (
                        answer["answer_text"] == "answer test"
                    ), f"Expected answer_text to be 'answer test', but got '{answer['answer_text']}'"
                break
            elif task_status["status"] == "FAILURE":
                pytest.fail(f"Task failed with error: {task_status.get('error')}")
            else:
                await asyncio.sleep(1)
        else:
            pytest.fail("Task did not complete within the allowed time.")
