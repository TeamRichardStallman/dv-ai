import httpx
from asgiref.sync import async_to_sync
from celery import Task

from app.core.celery_app import celery_app
from app.core.config import Config
from app.schemas.answer import AnswerRequestModel
from app.schemas.evaluation import EvaluationRequestModel
from app.schemas.question import QuestionsRequestModel
from app.services.interview_service import (
    process_answer_evaluation,
    process_interview_questions,
    process_overall_evaluation,
)
from app.utils.format import to_serializable


class BaseTaskWithAPICallback(Task):
    api_endpoint = ""

    def on_success(self, retval, task_id, args, kwargs):
        try:
            self.send_to_backend(retval)
        except Exception as e:
            print(f"API call failed: {str(e)}")

    def send_to_backend(self, result):
        try:
            with httpx.Client() as client:
                response = client.post(
                    f"{Config.BACK_API_URL}{self.api_endpoint}",
                    json=result,
                )
                response.raise_for_status()
        except Exception as http_error:
            raise RuntimeError(f"Error sending result to external server: {http_error}")


class AsyncProcessInterviewQuestions(BaseTaskWithAPICallback):
    api_endpoint = "/question/completion"


@celery_app.task(bind=True, base=AsyncProcessInterviewQuestions)
def async_process_interview_questions(self, interview_id: int, request_data: dict) -> str:
    request_data_obj = QuestionsRequestModel(**request_data)
    self.update_state(
        state="PROGRESS",
        meta={"message": f"Processing questions for interview {interview_id} in progress"},
    )

    try:
        result = async_to_sync(process_interview_questions)(interview_id, request_data_obj)
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
                "exc_type": type(e).__name__,
                "exc_message": str(e),
            },
        )
        raise RuntimeError(f"Error processing questions: {e}")


class AsyncProcessInterviewEvaluation(BaseTaskWithAPICallback):
    api_endpoint = "/evaluation/completion"


@celery_app.task(bind=True, base=AsyncProcessInterviewEvaluation)
def async_process_overall_evaluation(self, interview_id: int, request_data: dict) -> str:
    evaluation_data_obj = EvaluationRequestModel(**request_data)
    self.update_state(
        state="PROGRESS",
        meta={"message": f"Processing evaluation for interview {interview_id} in progress"},
    )
    try:

        result = process_overall_evaluation(interview_id, evaluation_data_obj)
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
                "exc_type": type(e).__name__,
                "exc_message": str(e),
            },
        )
        raise RuntimeError(f"Error processing evaluation: {e}")


class AsyncProcessAnswerEvaluation(BaseTaskWithAPICallback):
    api_endpoint = "/answer/evaluations"


@celery_app.task(bind=True, base=AsyncProcessAnswerEvaluation)
def async_process_answer_evaluation(self, interview_id: int, request_data: dict) -> str:
    answer_data_obj = AnswerRequestModel(**request_data)
    self.update_state(
        state="PROGRESS",
        meta={
            "message": f"Processing answer for question {answer_data_obj.question.question_id} in interview {interview_id} in progress"
        },
    )
    try:
        result = async_to_sync(process_answer_evaluation)(interview_id, answer_data_obj)
        serializable_result = to_serializable(result)
        self.update_state(
            state="SUCCESS",
            meta={
                "message": f"Answer processed for question {answer_data_obj.question.question_id} in interview {interview_id}!",
                "result": serializable_result,
            },
        )
        return serializable_result
    except Exception as e:
        self.update_state(
            state="FAILURE",
            meta={
                "message": f"Error processing evaluation for interview {interview_id}: {str(e)}",
                "exc_type": type(e).__name__,
                "exc_message": str(e),
            },
        )
        raise RuntimeError(f"Error processing evaluation: {e}")
