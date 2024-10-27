from pydantic import BaseModel
from typing import List


class Question(BaseModel):
    question_id: int
    question_text: str
    question_intent: str
    core_competency: List[str]
    model_answer: str

    class Config:
        schema_extra = {
            "example": {
                "question_id": 1,
                "question_text": "스타크래프트를 처음으로 접한 경험을 통해 어떻게 최고를 목표로 삼고 성취했는지 이야기해보세요.",
                "question_intent": "지원자의 목표 설정 및 성취 능력 파악",
                "core_competency": ["goal-setting", "achievement"],
                "model_answer": "초등학교 시절 스타크래프트를 처음 접한 후 매일 플레이를 통해 1등이 되기 위해 노력했습니다. 이를 통해 목표를 설정하고 끈질긴 노력을 통해 성취할 수 있는 능력을 길렀습니다.",
            }
        }


class QuestionsResponse(BaseModel):
    questions: List[Question]

    class Config:
        schema_extra = {
            "example": {
                "questions": [
                    {
                        "question_id": 1,
                        "question_text": "스타크래프트를 처음으로 접한 경험을 통해 어떻게 최고를 목표로 삼고 성취했는지 이야기해보세요.",
                        "question_intent": "지원자의 목표 설정 및 성취 능력 파악",
                        "core_competency": ["goal-setting", "achievement"],
                        "model_answer": "초등학교 시절 스타크래프트를 처음 접한 후 매일 플레이를 통해 1등이 되기 위해 노력했습니다. 이를 통해 목표를 설정하고 끈질긴 노력을 통해 성취할 수 있는 능력을 길렀습니다.",
                    },
                    {
                        "question_id": 2,
                        "question_text": "현재 백엔드 개발자로 성장하기 위해 어떤 노력을 기울이고 있는지 설명해주세요.",
                        "question_intent": "지원자의 성장 의지 및 노력 파악",
                        "core_competency": ["self-improvement", "backend development"],
                        "model_answer": "컴퓨터 기초, 웹, 언어 공부 및 다양한 프로젝트, 인턴 등을 통해 백엔드 개발자로 성장하기 위해 노력하고 있습니다.",
                    },
                ]
            }
        }
