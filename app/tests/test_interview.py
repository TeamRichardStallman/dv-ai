import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
@pytest.mark.parametrize("interview_method", ["chat", "voice"])
async def test_create_interview_questions(interview_method):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/interview/abc/questions",
            json={
                "user_id": 1,
                "interview_mode": "real",
                "interview_type": "technical",
                "interview_method": interview_method,
                "job_role": "ai",
                "question_count": 1,
                "file_paths": ["cover-letters/cover_letter_01.txt"],
            },
        )
    assert response.status_code == 200
    assert "questions" in response.json()


@pytest.mark.asyncio
@pytest.mark.parametrize("interview_method", ["chat", "voice"])
async def test_create_answer_text_from_answer_audio(interview_method):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/interview/1/answer/1",
            json={
                "interview_method": interview_method,
                "user_id": 0,
                "answer": {
                    "answer_text": "answer test",
                    "s3_audio_url": "test/questions/audio_1.mp3",
                    "s3_video_url": "string",
                },
            },
        )
    assert response.status_code == 200
    assert "answer_text" in response.json()["answer"]
