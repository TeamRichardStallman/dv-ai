from app.models.evaluation_response import EvaluationRequest
from app.prompts.prompt import Real_Tech_Eval, Real_Personal_Eval, General_Tech_Eval


def generate_evaluation_prompt(user_data: EvaluationRequest):
    try:
        job_role = user_data.job_role
        interview_type = user_data.interview_type
        interview_mode = user_data.interview_mode
    except KeyError as e:
        raise KeyError(f"Missing required key in user_data: {e}")

    if interview_mode == 'real':
        if interview_type == 'technical':
            generation_prompt = Real_Tech_Eval
        elif interview_type == 'personal':
            generation_prompt = Real_Personal_Eval
    elif interview_mode == 'general':
        generation_prompt = General_Tech_Eval
    else:
        raise ValueError(f"Unknown interview_mode: {interview_mode}")

    try:
        prompt = generation_prompt.format(
            job_role=job_role,
            interview_type=interview_type
        )
    except KeyError as e:
        raise KeyError(f"Missing key during prompt formatting: {e}")

    return prompt
