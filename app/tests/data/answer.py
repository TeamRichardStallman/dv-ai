from app.schemas.answer import AnswerRequestModel, TechnicalAnswerResponseModel

ANSWER_REQUEST_DATA: AnswerRequestModel = {}

ANSWER_RESPONSE_DATA: TechnicalAnswerResponseModel = {
    "user_id": 1,
    "interview_id": 1,
    "question_id": 1,
    "interview_method": "voice",
    "answer": {
        "answer_text": "AI 대회 준비 과정에서 저는 컴퓨터 비전 분야의 YOLO(You Only Look Once) 알고리즘에 깊은 관심을 가지게 되었습니다. 초기에 AI 알고리즘 코드 작성에 어려움을 겪었지만, 정보통신공학과 김교수님께 직접 이메일로 조언을 요청했습니다. 교수님께서는 객체 탐지 알고리즘의 기본 원리와 PyTorch를 활용한 구현 방법에 대해 상세히 설명해주셨습니다.\n\n특히 제 선배인 박지훈 연구원은 실제 프로젝트에서 YOLO v5 모델을 적용한 경험을 공유해주며, 데이터 전처리, 모델 fine-tuning, 성능 평가 등 실질적인 팁을 알려주었습니다. 이러한 멘토링을 통해 저는 점진적으로 알고리즘에 대한 이해를 깊게 할 수 있었고, 결과적으로 AI 대회에서 객체 탐지 모델을 성공적으로 구현할 수 있었습니다.",
        "s3_audio_url": "test/users/1/interviews/abc/questions/answer-1.mp3",
        "s3_video_url": None,
        "scores": {
            "text_scores": {
                "appropriate_response": {
                    "score": 9,
                    "rationale": "질문의 의도를 정확히 파악하고 구체적인 경험을 상세히 설명함",
                },
                "logical_flow": {"score": 8, "rationale": "멘토링 과정과 학습 경험을 논리적으로 전개함"},
                "key_terms": {"score": 9, "rationale": "AI 알고리즘, 멘토링, 대회 경험 등 핵심 용어를 적절히 활용"},
                "consistency": {"score": 8, "rationale": "전체적인 내용의 일관성이 높음"},
                "grammatical_errors": {"score": 9, "rationale": "문법적 오류 없이 명확하게 작성됨"},
            },
            "voice_scores": {
                "wpm": {"score": 7, "rationale": "적절한 속도로 말하나 약간의 개선 여지 있음"},
                "stutter": {"score": 8, "rationale": "대부분 유창하게 말하나 간혹 주저함"},
                "pronunciation": {"score": 9, "rationale": "명확하고 정확한 발음"},
            },
        },
        "feedback": {
            "strengths": "AI 알고리즘에 대한 깊이 있는 이해와 멘토링 과정의 구체적인 설명",
            "improvement": "기술적 세부사항에 대해 더 깊이 있는 기술 가능",
            "suggestion": "향후 프로젝트에서는 더 복잡한 알고리즘 적용을 고려해볼 것",
        },
    },
}
