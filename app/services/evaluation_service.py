from app.prompts.chat.chat_evaluation import GENERAL_TECH_CHAT_EVAL, REAL_PERSONAL_CHAT_EVAL, REAL_TECH_CHAT_EVAL
from app.prompts.voice.voice_evaluation import GENERAL_TECH_VOICE_EVAL, REAL_PERSONAL_VOICE_EVAL, REAL_TECH_VOICE_EVAL
from app.schemas.evaluation import EvaluationRequest, SingleEvaluationRequest


def generate_evaluation_prompt(interview_id: int, user_data: EvaluationRequest) -> str:
    try:
        user_id = user_data.user_id
        job_role = user_data.job_role
        interview_type = user_data.interview_type
        interview_mode = user_data.interview_mode
    except KeyError as e:
        raise KeyError(f"Missing required key in user_data: {e}")

    if interview_mode == "real":
        if interview_type == "technical":
            generation_prompt = REAL_TECH_CHAT_EVAL
        elif interview_type == "personal":
            generation_prompt = REAL_PERSONAL_CHAT_EVAL
    elif interview_mode == "general":
        generation_prompt = GENERAL_TECH_CHAT_EVAL
    else:
        raise ValueError(f"Unknown interview_mode: {interview_mode}")

    try:
        prompt = generation_prompt.format(
            job_role=job_role, interview_type=interview_type, user_id=user_id, interview_id=interview_id
        )
    except KeyError as e:
        raise KeyError(f"Missing key during prompt formatting: {e}")

    return prompt


def generate_single_evaluation_prompt(interview_id: int, request_data: SingleEvaluationRequest, wpm: int) -> str:
    user_id = request_data.user_id
    job_role = request_data.job_role
    interview_type = request_data.interview_type
    interview_mode = request_data.interview_mode
    interview_method = request_data.interview_method
    question_text = request_data.question.question
    answer_text = request_data.answer.answer_text

    if interview_method == "chat":
        if interview_mode == "real":
            if interview_type == "technical":
                generation_prompt = REAL_TECH_CHAT_EVAL
            elif interview_type == "personal":
                generation_prompt = REAL_PERSONAL_CHAT_EVAL
        elif interview_mode == "general":
            generation_prompt = GENERAL_TECH_CHAT_EVAL
        else:
            raise ValueError(f"Unknown interview_mode: {interview_mode}")

    else:
        if interview_mode == "real":
            if interview_type == "technical":
                generation_prompt = REAL_TECH_VOICE_EVAL
            elif interview_type == "personal":
                generation_prompt = REAL_PERSONAL_VOICE_EVAL
        elif interview_mode == "general":
            generation_prompt = GENERAL_TECH_VOICE_EVAL
        else:
            raise ValueError(f"Unknown interview_mode: {interview_mode}")

    try:
        prompt = generation_prompt.format(
            user_id=user_id,
            job_role=job_role,
            interview_type=interview_type,
            interview_id=interview_id,
            question_text=question_text,
            answer_text=answer_text,
            wpm=wpm,
        )
    except KeyError as e:
        raise KeyError(f"Missing key during prompt formatting: {e}")

    return prompt
