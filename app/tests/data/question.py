from typing import List
from app.schemas.question import Question

QUESTIONS_RESPONSE_DATA: List[Question] = {
    "questions": [
        {
            "question_id": 1,
            "question": {
                "question_text": "AI 대회에 출전하면서 교수님과 선배님들의 도움을 받았던 구체적인 경험과 그 과정에서 어떤 AI 알고리즘을 연구했는지에 대해 자세히 설명해 주시겠어요?",
                "s3_audio_url": "test/users/1/interviews/abc/questions/question-1.mp3",
                "s3_video_url": None,
            },
            "question_excerpt": "AI 알고리즘 코드를 짜본 경험이 없었기 때문에 대회 진행에 어려움을 겪었습니다. 그리하여 AI 개발에 능숙하신 교수님과 선배님들에게 이메일을 보내 적극적으로 도움을 요청하였습니다.",
            "question_intent": "AI 대회에서의 경험과 멘토링 과정에서의 학습 능력을 평가하기 위함입니다.",
            "key_terms": ["AI 알고리즘", "멘토링", "대회 경험", "학습 과정", "문제 해결"],
        },
        {
            "question_id": 2,
            "question": {
                "question_text": "전선 탐지 알고리즘 프로젝트에서 빛 번짐 문제를 해결하기 위해 시도한 방법과 그 결과에 대해 좀 더 구체적으로 말씀해 주시겠어요?",
                "s3_audio_url": "test/users/1/interviews/abc/questions/question-2.mp3",
                "s3_video_url": None,
            },
            "question_excerpt": "빛 번짐을 제거할 수 있는 코드를 적용하여 데이터를 전처리 하자는 의견이 나왔습니다.",
            "question_intent": "AI 알고리즘의 문제 해결 능력과 창의적인 접근 방식을 평가하기 위함입니다.",
            "key_terms": ["전선 탐지", "AI 알고리즘", "문제 해결", "데이터 전처리", "효율성"],
        },
        {
            "question_id": 3,
            "question": {
                "question_text": "Digital Transformation을 위한 자동화 프로그램을 개발하면서 어떤 기술적 요소를 고려했는지, 그리고 이 과정에서 직면한 도전 과제는 무엇이었는지 설명해 주시겠어요?",
                "s3_audio_url": "test/users/1/interviews/abc/questions/question-3.mp3",
                "s3_video_url": None,
            },
            "question_excerpt": "이를 해결하기 위해 자동화 프로그램을 제작하여 데이터 수집 시스템을 구축하기를 대표님께 건의했습니다.",
            "question_intent": "Digital Transformation 관련 기술적 이해와 문제 해결 능력을 평가하기 위함입니다.",
            "key_terms": ["Digital Transformation", "자동화 프로그램", "데이터 수집", "기술적 요소", "문제 해결"],
        },
    ]
}
