from asgiref.sync import async_to_sync

from app.core.celery_app import celery_app
from app.schemas.answer import AnswerRequest
from app.schemas.evaluation import EvaluationRequest
from app.schemas.question import QuestionsRequest
from app.services.interview_service import process_answer, process_evaluation, process_questions
from app.services.s3_service import S3Service
from app.services.stt_service import get_stt_service
from app.services.tts_service import get_tts_service
from app.utils.format import to_serializable


@celery_app.task(bind=True)
def async_process_questions(self, interview_id: int, request_data: dict) -> str:
    self.update_state(
        state="PROGRESS",
        meta={"message": f"Processing questions for interview {interview_id} in progress"},
    )

    try:
        request_data_obj = QuestionsRequest(**request_data)

        s3_service = S3Service()
        tts_service = get_tts_service(model_name="openai")

        result = async_to_sync(process_questions)(interview_id, request_data_obj, s3_service, tts_service)

        self.update_state(
            state="SUCCESS",
            meta={
                "message": f"Questions for interview {interview_id} successfully processed",
                "result": result.dict() if hasattr(result, "dict") else result,
            },
        )
        return result.dict() if hasattr(result, "dict") else result

    except Exception as e:
        self.update_state(
            state="FAILURE",
            meta={
                "message": f"Error processing questions for interview {interview_id}: {str(e)}",
            },
        )
        raise RuntimeError(f"Error processing questions: {e}")


# 비동기 작업: 평가 처리
@celery_app.task(bind=True)
def async_process_evaluation(self, interview_id: int, request_data: dict) -> str:
    self.update_state(
        state="PROGRESS",
        meta={"message": f"Processing evaluation for interview {interview_id} in progress"},
    )
    try:
        evaluation_data_obj = EvaluationRequest(**request_data)

        result = process_evaluation(interview_id, evaluation_data_obj)

        self.update_state(
            state="SUCCESS",
            meta={
                "message": f"Evaluation for interview {interview_id} successfully processed",
                "result": result.dict() if hasattr(result, "dict") else result,
            },
        )
        return result.dict() if hasattr(result, "dict") else result
    except Exception as e:
        self.update_state(
            state="FAILURE",
            meta={
                "message": f"Error processing evaluation for interview {interview_id}: {str(e)}",
            },
        )
        raise RuntimeError(f"Error processing evaluation: {e}")


# 비동기 작업: 음성에서 텍스트 변환
@celery_app.task(bind=True)
def async_process_answer(self, interview_id: int, question_id: int, request_data: dict) -> str:
    self.update_state(
        state="PROGRESS",
        meta={"message": f"Processing answer for question {question_id} in interview {interview_id} in progress"},
    )

    try:
        answer_data_obj = AnswerRequest(**request_data)

        s3_service = S3Service()
        stt_service = get_stt_service(model_name="whisper")

        result = async_to_sync(process_answer)(interview_id, question_id, answer_data_obj, s3_service, stt_service)

        serializable_result = to_serializable(result)

        self.update_state(
            state="SUCCESS",
            meta={
                "message": f"Answer processed for question {question_id} in interview {interview_id}!",
                "result": serializable_result,
            },
        )
        return serializable_result
    except Exception as e:
        self.update_state(
            state="FAILURE",
            meta={
                "message": f"Error processing evaluation for interview {interview_id}: {str(e)}",
                "error": repr(e),
            },
        )
        raise RuntimeError(f"Error processing evaluation: {e}")
