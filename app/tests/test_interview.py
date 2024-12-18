import asyncio
from typing import Any, Dict
from unittest.mock import patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.tests.data.evaluation import EVALUATION_REQUEST_DATA
from app.tests.utils.tasks import retry_task_execution

BASE_URL = "http://test"


def validate_task_response(response_data: Dict[str, Any]) -> None:
    """Validate the structure of the task response"""
    required_fields = {"message", "task_id", "status"}
    missing_fields = required_fields - set(response_data.keys())

    if missing_fields:
        raise AssertionError(f"Missing required fields in response: {missing_fields}")

    assert isinstance(
        response_data["message"], str
    ), f"Expected 'message' to be string, got {type(response_data['message'])}"
    assert isinstance(
        response_data["task_id"], str
    ), f"Expected 'task_id' to be string, got {type(response_data['task_id'])}"
    assert (
        response_data["status"] == "processing"
    ), f"Expected status to be 'processing', got '{response_data['status']}'"


@patch("app.services.tasks.BaseTaskWithAPICallback.send_to_backend", return_value=None)
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "interview_id, interview_mode, interview_type, interview_method, question_count, file_paths",
    [
        (1, "real", "technical", "chat", 1, ["cover-letters/SK_AI_01.txt"]),
        (2, "real", "technical", "voice", 1, ["cover-letters/SK_AI_01.txt"]),
        (3, "real", "personal", "chat", 1, ["cover-letters/SK_AI_01.txt"]),
        (4, "real", "personal", "voice", 1, ["cover-letters/SK_AI_01.txt"]),
        (5, "general", "technical", "chat", 1, []),
        (6, "general", "technical", "voice", 1, []),
    ],
)
async def test_create_interview_questions(
    mock_send_to_backend, interview_id, interview_mode, interview_type, interview_method, question_count, file_paths
):
    mock_send_to_backend.return_value = {"success": True, "message": "Successfully sent to backend"}
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

        assert (
            response.status_code == 200
        ), f"Expected status code 200, got {response.status_code}. Response: {response.text}"

        response_json = response.json()
        validate_task_response(response_json)
        task_id = response_json["task_id"]

        for _ in range(60):
            task_response = await ac.get(f"/tasks/{task_id}")
            assert task_response.status_code == 200, f"Task status check failed with status {task_response.status_code}"

            task_status = task_response.json()

            if task_status["status"] == "SUCCESS":
                result = await retry_task_execution(ac, task_id)

                assert "questions" in result, "Result missing 'questions' field"
                questions = result["questions"]

                assert isinstance(questions, list), f"Expected questions to be a list, got {type(questions)}"
                assert len(questions) == question_count, f"Expected {question_count} questions, got {len(questions)}"

                for idx, question in enumerate(questions):
                    assert isinstance(question, dict), f"Question {idx} is not a dictionary"

                    required_fields = ["question", "question_intent", "key_terms"]
                    for field in required_fields:
                        assert field in question, f"Question {idx} missing required field '{field}'"

                    question_detail = question["question"]
                    assert isinstance(
                        question_detail, dict
                    ), f"Question {idx}'s 'question' field should be a dictionary"
                    assert (
                        "question_text" in question_detail
                    ), f"Question {idx}'s question field missing 'question_text'"
                    assert isinstance(
                        question_detail["question_text"], str
                    ), f"Question {idx}'s question_text should be a string"

                    # Validate key_terms
                    assert isinstance(question["key_terms"], list), f"Question {idx}'s key_terms should be a list"

                    # Validate question_intent
                    assert isinstance(
                        question["question_intent"], str
                    ), f"Question {idx}'s question_intent should be a string"
                break

            elif task_status["status"] == "FAILURE":
                error_msg = task_status.get("error", "No error message provided")
                pytest.fail(f"Task failed with error: {error_msg}")
            else:
                await asyncio.sleep(1)
        else:
            pytest.fail("Task did not complete within 60 seconds timeout")


@patch("app.services.tasks.BaseTaskWithAPICallback.send_to_backend", return_value=None)
@pytest.mark.asyncio
async def test_create_overall_evaluation(mock_send_to_backend):
    mock_send_to_backend.return_value = {"success": True, "message": "Successfully sent to backend"}
    evaluation_request_data = EVALUATION_REQUEST_DATA

    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as ac:
        response = await ac.post("/interview/1/evaluation", json=evaluation_request_data)
        assert (
            response.status_code == 200
        ), f"Expected status code 200, got {response.status_code}. Response: {response.text}"

        response_json = response.json()
        validate_task_response(response_json)
        task_id = response_json["task_id"]

        for _ in range(300):
            task_response = await ac.get(f"/tasks/{task_id}")
            assert task_response.status_code == 200, f"Task status check failed with status {task_response.status_code}"

            task_status = task_response.json()

            if task_status["status"] == "SUCCESS":
                result = await retry_task_execution(ac, task_id)
                assert "overall_evaluation" in result, "Result missing 'overall_evaluation' field"
                overall_evaluation = result["overall_evaluation"]

                # Validate evaluation structure
                # Validate overall evaluation structure
                required_fields = ["text_overall", "voice_overall"]
                for field in required_fields:
                    assert field in overall_evaluation, f"Overall evaluation missing required field '{field}'"

                    if field == "text_overall":
                        text_overall = overall_evaluation["text_overall"]
                        assert isinstance(
                            text_overall, dict
                        ), f"Expected text_overall to be dictionary, got {type(text_overall)}"

                        # Validate text_overall structure
                        text_required_fields = ["job_fit", "growth_potential", "work_attitude", "technical_depth"]
                        for text_field in text_required_fields:
                            assert text_field in text_overall, f"text_overall missing required field '{text_field}'"

                            score_detail = text_overall[text_field]
                            assert isinstance(
                                score_detail, dict
                            ), f"Expected {text_field} to be dictionary, got {type(score_detail)}"
                            assert "rationale" in score_detail, f"{text_field} missing 'rationale' field"
                            assert "score" in score_detail, f"{text_field} missing 'score' field"
                            assert isinstance(
                                score_detail["score"], (int, float)
                            ), f"Expected {text_field} score to be number, got {type(score_detail['score'])}"

                    if field == "voice_overall" and overall_evaluation["voice_overall"] is not None:
                        voice_overall = overall_evaluation["voice_overall"]
                        assert isinstance(
                            voice_overall, dict
                        ), f"Expected voice_overall to be dictionary, got {type(voice_overall)}"

                        # Validate voice_overall structure
                        voice_required_fields = ["fluency", "clarity", "word_repetition"]
                        for voice_field in voice_required_fields:
                            assert voice_field in voice_overall, f"voice_overall missing required field '{voice_field}'"

                            score_detail = voice_overall[voice_field]
                            assert isinstance(
                                score_detail, dict
                            ), f"Expected {voice_field} to be dictionary, got {type(score_detail)}"
                            assert "rationale" in score_detail, f"{voice_field} missing 'rationale' field"
                            assert "score" in score_detail, f"{voice_field} missing 'score' field"
                            assert isinstance(
                                score_detail["score"], (int, float)
                            ), f"Expected {voice_field} score to be number, got {type(score_detail['score'])}"
                break

            elif task_status["status"] == "FAILURE":
                error_msg = task_status.get("error", "No error message provided")
                pytest.fail(f"Task failed with error: {error_msg}")
            else:
                await asyncio.sleep(1)
        else:
            pytest.fail("Task did not complete within 300 seconds timeout")


@patch("app.services.tasks.BaseTaskWithAPICallback.send_to_backend", return_value=None)
@pytest.mark.asyncio
@pytest.mark.parametrize("interview_mode", ["real", "general"])
@pytest.mark.parametrize("interview_type", ["technical", "personal"])
@pytest.mark.parametrize("interview_method", ["chat", "voice"])
async def test_create_answer_evaluation(mock_send_to_backend, interview_mode, interview_type, interview_method):
    mock_send_to_backend.return_value = {"success": True, "message": "Successfully sent to backend"}
    answer_data = {
        "user_id": 1,
        "interview_mode": interview_mode,
        "interview_type": interview_type,
        "interview_method": interview_method,
        "job_role": "ai",
        "question": {
            "question_id": 1,
            "question": {"question_text": "string", "s3_audio_url": "string", "s3_video_url": "string"},
            "question_excerpt": "string",
            "question_intent": "string",
            "key_terms": ["string"],
        },
        "answer": {
            "answer_text": "테스트용 답변입니다.",
            "s3_audio_url": "test/questions/audio_1.mp3",
            "s3_video_url": "string",
        },
        "file_path": "cover-letters/SK_AI_01.txt",
    }

    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as ac:
        response = await ac.post("/interview/1/answer/1", json=answer_data)
        assert (
            response.status_code == 200
        ), f"Expected status code 200, got {response.status_code}. Response: {response.text}"

        response_json = response.json()
        validate_task_response(response_json)
        task_id = response_json["task_id"]

        for _ in range(60):
            task_response = await ac.get(f"/tasks/{task_id}")
            assert task_response.status_code == 200, f"Task status check failed with status {task_response.status_code}"

            task_status = task_response.json()

            if task_status["status"] == "SUCCESS":
                result = await retry_task_execution(ac, task_id)

                assert "answer" in result, "Result missing 'answer' field"
                answer = result["answer"]

                # Validate answer structure
                assert "answer_text" in answer, "Answer missing 'answer_text' field"
                assert isinstance(
                    answer["answer_text"], str
                ), f"Expected answer_text to be string, got {type(answer['answer_text'])}"
                break

            elif task_status["status"] == "FAILURE":
                error_msg = task_status.get("error", "No error message provided")
                pytest.fail(f"Task failed with error: {error_msg}")
            else:
                await asyncio.sleep(1)
        else:
            pytest.fail("Task did not complete within 60 seconds timeout")
