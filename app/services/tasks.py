from asgiref.sync import async_to_sync

from app.core.celery_app import celery_app
from app.schemas.answer import AnswerRequestModel
from app.schemas.evaluation import EvaluationRequestModel
from app.schemas.question import QuestionsRequestModel
from app.services.interview_service import (
    process_answer_evaluation,
    process_interview_evaluation,
    process_interview_questions,
)
from app.services.s3_service import S3Service
from app.services.stt_service import get_stt_service
from app.services.tts_service import get_tts_service
from app.utils.format import to_serializable


@celery_app.task(bind=True)
def async_process_interview_questions(self, interview_id: int, request_data: dict) -> str:
    self.update_state(
        state="PROGRESS",
        meta={"message": f"Processing questions for interview {interview_id} in progress"},
    )

    try:
        request_data_obj = QuestionsRequestModel(**request_data)

        s3_service = S3Service()
        tts_service = get_tts_service(model_name="openai")

        result = async_to_sync(process_interview_questions)(interview_id, request_data_obj, s3_service, tts_service)

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


@celery_app.task(bind=True)
def async_process_interview_evaluation(self, interview_id: int, request_data: dict) -> str:
    self.update_state(
        state="PROGRESS",
        meta={"message": f"Processing evaluation for interview {interview_id} in progress"},
    )
    try:
        evaluation_data_obj = EvaluationRequestModel(**request_data)

        result = process_interview_evaluation(interview_id, evaluation_data_obj)

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


@celery_app.task(bind=True)
def async_process_answer_evaluation(self, interview_id: int, question_id: int, request_data: dict) -> str:
    self.update_state(
        state="PROGRESS",
        meta={"message": f"Processing answer for question {question_id} in interview {interview_id} in progress"},
    )

    try:
        answer_data_obj = AnswerRequestModel(**request_data)

        s3_service = S3Service()
        stt_service = get_stt_service(model_name="whisper")

        result = async_to_sync(process_answer_evaluation)(
            interview_id, question_id, answer_data_obj, s3_service, stt_service
        )

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
