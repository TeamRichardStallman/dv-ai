from langchain_core.prompts import load_prompt

from app.schemas.question import QuestionsRequestModel


def generate_questions_prompt(interview_id: int, user_data: QuestionsRequestModel) -> str:
    # Extract required fields from user_data
    user_id = user_data.user_id
    job_role = user_data.job_role
    interview_type = user_data.interview_type
    interview_mode = user_data.interview_mode
    question_count = user_data.question_count

    # Map interview_mode and interview_type to corresponding prompt files
    prompt_map = {
        ("real", "technical"): "app/prompts/real_tech.yaml",
        ("real", "personal"): "app/prompts/real_personal.yaml",
        ("general", "technical"): "app/prompts/general_tech.yaml",
    }

    prompt_path = prompt_map.get((interview_mode, interview_type))

    if not prompt_path:
        raise ValueError(
            f"Invalid combination of interview_mode '{interview_mode}' and interview_type '{interview_type}'"
        )

    # Load and format the prompt
    generation_prompt = load_prompt(prompt_path)
    return generation_prompt.format(
        job_role=job_role, question_count=question_count, user_id=user_id, interview_id=interview_id
    )
