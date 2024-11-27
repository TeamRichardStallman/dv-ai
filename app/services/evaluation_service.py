from app.prompts.evaluation import GENERAL_TECH_EVAL, REAL_PERSONAL_EVAL, REAL_TECH_EVAL
from app.schemas.evaluation import EvaluationRequest


def generate_evaluation_prompt(user_data: EvaluationRequest):
    try:
        job_role = user_data.job_role
        interview_type = user_data.interview_type
        interview_mode = user_data.interview_mode
    except KeyError as e:
        raise KeyError(f"Missing required key in user_data: {e}")

    if interview_mode == "real":
        if interview_type == "technical":
            generation_prompt = REAL_TECH_EVAL
        elif interview_type == "personal":
            generation_prompt = REAL_PERSONAL_EVAL
    elif interview_mode == "general":
        generation_prompt = GENERAL_TECH_EVAL
    else:
        raise ValueError(f"Unknown interview_mode: {interview_mode}")

    try:
        prompt = generation_prompt.format(job_role=job_role, interview_type=interview_type)
    except KeyError as e:
        raise KeyError(f"Missing key during prompt formatting: {e}")

    return prompt
