import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
@pytest.mark.parametrize("question_count", [1])
@pytest.mark.parametrize("interview_method", ["chat", "voice"])
@pytest.mark.parametrize("interview_type", ["technical", "personal"])
@pytest.mark.parametrize("interview_mode", ["real"])
async def test_create_interview_questions_with_real(interview_mode, interview_type, interview_method, question_count):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/interview/1/questions",
            json={
                "user_id": 1,
                "interview_mode": interview_mode,
                "interview_type": interview_type,
                "interview_method": interview_method,
                "job_role": "ai",
                "question_count": question_count,
                "file_paths": ["cover-letters/SK_AI_01.txt"],
            },
        )
    assert response.status_code == 200
    response_json = response.json()
    assert "questions" in response_json
    questions = response_json["questions"]
    assert len(questions) == question_count, f"Expected {question_count} questions, but got {len(questions)}"


@pytest.mark.asyncio
@pytest.mark.parametrize("question_count", [1])
@pytest.mark.parametrize("interview_method", ["chat"])
@pytest.mark.parametrize("interview_type", ["technical"])
@pytest.mark.parametrize("interview_mode", ["general"])
async def test_create_interview_questions_with_general(
    interview_mode, interview_type, interview_method, question_count
):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/interview/1/questions",
            json={
                "user_id": 1,
                "interview_mode": interview_mode,
                "interview_type": interview_type,
                "interview_method": interview_method,
                "job_role": "ai",
                "question_count": question_count,
                "file_paths": [],
            },
        )
    assert response.status_code == 200
    response_json = response.json()
    assert "questions" in response_json
    questions = response_json["questions"]
    assert len(questions) == question_count, f"Expected {question_count} questions, but got {len(questions)}"


@pytest.mark.asyncio
async def test_create_interview_evaluation():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/interview/1/evaluation",
            json={
                "user_id": 1,
                "interview_mode": "real",
                "interview_type": "technical",
                "interview_method": "voice",
                "job_role": "ai",
                "questions": {
                    "questions": [
                        {
                            "question_id": 1,
                            "question": {
                                "question_text": "설명해주세요. 딥러닝에서 과적합(Overfitting)을 방지하는 주요 전략은 무엇입니까?",
                                "s3_audio_url": None,
                                "s3_video_url": None,
                            },
                            "question_excerpt": "딥러닝 과적합 방지 전략",
                            "question_intent": "기술적 깊이와 문제 해결 능력 평가",
                            "key_terms": ["regularization", "dropout", "early stopping", "data augmentation"],
                        }
                    ]
                },
                "answers": [
                    {
                        "question_id": 1,
                        "answer": {
                            "answer_text": "딥러닝에서 과적합을 방지하기 위한 주요 전략은 여러 가지가 있습니다. 첫째, 드롭아웃(Dropout) 기법을 사용하여 네트워크의 일부 뉴런을 임의로 비활성화함으로써 모델이 특정 피처에 과도하게 의존하는 것을 방지할 수 있습니다. 둘째, L1, L2 정규화를 통해 가중치의 크기를 제한하고 모델의 복잡성을 줄일 수 있습니다. 또한 조기 종료(Early Stopping) 기법을 사용하여 검증 손실이 증가하기 시작할 때 학습을 중단할 수 있습니다. 데이터 증강(Data Augmentation)도 중요한 전략으로, 학습 데이터의 다양성을 높여 모델의 일반화 능력을 개선합니다.",
                            "s3_audio_url": None,
                            "s3_video_url": None,
                            "scores": {
                                "text_scores": {
                                    "appropriate_response": {
                                        "score": 9,
                                        "rationale": "질문에 직접적이고 명확하게 답변, 관련 전략들을 구체적으로 설명",
                                    },
                                    "logical_flow": {"score": 8, "rationale": "논리적이고 체계적인 설명 구조"},
                                    "key_terms": {
                                        "score": 10,
                                        "rationale": "모든 핵심 용어(Dropout, Regularization, Early Stopping, Data Augmentation) 적절히 언급",
                                    },
                                    "consistency": {"score": 9, "rationale": "일관된 주제와 기술적 깊이 유지"},
                                    "grammatical_errors": {
                                        "score": 10,
                                        "rationale": "문법적으로 완벽하고 명확한 문장 구조",
                                    },
                                },
                                "voice_scores": {
                                    "wpm": {"score": 8, "rationale": "적절한 말하기 속도, 정보 전달에 효과적"},
                                    "stutter": {"score": 9, "rationale": "거의 막힘없이 유창하게 대답"},
                                    "pronunciation": {"score": 9, "rationale": "명확하고 정확한 발음"},
                                },
                            },
                            "feedback": {
                                "strengths": "기술적 개념에 대한 깊은 이해와 명확한 설명력",
                                "improvement": "더 구체적인 실제 사례나 구현 경험 추가",
                                "suggestion": "각 전략의 장단점에 대해 좀 더 심층적으로 논의",
                            },
                        },
                    }
                ],
                "file_paths": ["cover-letters/SK_AI.txt"],
            },
        )
    assert response.status_code == 200
    assert "overall_evaluation" in response.json()
    assert "text_overall" in response.json()["overall_evaluation"]
    assert "voice_overall" in response.json()["overall_evaluation"]


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
