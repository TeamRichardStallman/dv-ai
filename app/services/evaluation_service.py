from langchain_core.prompts import PromptTemplate

from app.prompts.chat.chat_overall import GENERAL_TECH_CHAT_OVER, REAL_PERSONAL_CHAT_OVER, REAL_TECH_CHAT_OVER
from app.prompts.voice.voice_overall import GENERAL_TECH_VOICE_OVER, REAL_PERSONAL_VOICE_OVER, REAL_TECH_VOICE_OVER
from app.schemas.evaluation import EvaluationRequestModel

from langchain_core.prompts import PromptTemplate


def generate_interview_evaluation_prompt(interview_id: int, request_data: EvaluationRequestModel) -> str:
    try:
        user_id = request_data.user_id
        job_role = request_data.job_role
        interview_method = request_data.interview_method
        interview_type = request_data.interview_type
        interview_mode = request_data.interview_mode

    except KeyError as e:
        raise KeyError(f"Missing required key in request_data: {e}")

    if interview_method == "chat":
        if interview_mode == "real":
            if interview_type == "technical":
                generation_prompt = REAL_TECH_CHAT_OVER
            elif interview_type == "personal":
                generation_prompt = REAL_PERSONAL_CHAT_OVER
        elif interview_mode == "general":
            generation_prompt = GENERAL_TECH_CHAT_OVER
        else:
            raise ValueError(f"Unknown interview_mode: {interview_mode}")

    else:
        if interview_mode == "real":
            if interview_type == "technical":
                generation_prompt = REAL_TECH_VOICE_OVER
            elif interview_type == "personal":
                generation_prompt = REAL_PERSONAL_VOICE_OVER
        elif interview_mode == "general":
            generation_prompt = GENERAL_TECH_VOICE_OVER
        else:
            raise ValueError(f"Unknown interview_mode: {interview_mode}")
    generation_prompt = PromptTemplate.from_template(generation_prompt)
    try:
        prompt = generation_prompt.format(
            job_role=job_role,
            interview_type=interview_type,
            user_id=user_id,
            interview_id=interview_id,
        )
    except KeyError as e:
        raise KeyError(f"Missing key during prompt formatting: {e}")

    return prompt
