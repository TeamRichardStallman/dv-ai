import time

from app.core.celery_config import celery_app


# 비동기 작업: 인터뷰 질문 처리
@celery_app.task
def async_process_questions(interview_id: int, data: dict) -> str:
    # 긴 작업 예시
    time.sleep(10)  # 처리 시간 시뮬레이션
    return f"Questions processed for interview {interview_id}!"


# 비동기 작업: 평가 처리
@celery_app.task
def async_process_evaluation(interview_id: int, data: dict) -> str:
    time.sleep(5)  # 처리 시간 시뮬레이션
    return f"Evaluation completed for interview {interview_id}!"


# 비동기 작업: 음성에서 텍스트 변환
@celery_app.task
def async_process_answer(interview_id: int, question_id: int, data: dict) -> str:
    time.sleep(7)  # 처리 시간 시뮬레이션
    return f"Answer processed for question {question_id} in interview {interview_id}!"
