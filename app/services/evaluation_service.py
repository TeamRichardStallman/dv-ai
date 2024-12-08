from app.schemas.evaluation import EvaluationRequest
from langchain_core.prompts import load_prompt


def generate_evaluation_prompt(interview_id: int, user_data: EvaluationRequest) -> str:
    user_id = user_data.user_id
    job_role = user_data.job_role
    interview_type = user_data.interview_type
    interview_mode = user_data.interview_mode

    prompt_map = {
        ("real", "technical"): "app/prompts/real_tech_eval.yaml",
        ("real", "personal"): "app/prompts/real_personal_eval.yaml",
        ("general", "technical"): "app/prompts/general_tech_eval.yaml"
    }

    prompt_path = prompt_map.get((interview_mode, interview_type))

    if not prompt_path:
        raise ValueError(f"Invalid combination of interview_mode '{interview_mode}' and interview_type '{interview_type}'")

    generation_prompt = load_prompt(prompt_path)
    return generation_prompt.format(
        job_role=job_role,
        interview_type=interview_type,
        user_id=user_id,
        interview_id=interview_id
    )