from langchain_core.prompts import load_prompt, PromptTemplate
from app.schemas.question import QuestionsRequestModel


# Predefine the prompt mapping for clarity and efficiency
PROMPT_MAP = {
    ("real", "technical"): "app/prompts/real_tech.yaml",
    ("real", "personal"): "app/prompts/real_personal.yaml",
    ("general", "technical"): "app/prompts/general_tech.yaml",
}


def generate_questions_prompt(user_data: QuestionsRequestModel) -> PromptTemplate:
    """Generate a prompt template based on interview mode and type."""
    prompt_path = PROMPT_MAP.get((user_data.interview_mode, user_data.interview_type))

    if not prompt_path:
        raise ValueError(
            f"Invalid combination of interview_mode '{user_data.interview_mode}' "
            f"and interview_type '{user_data.interview_type}'"
        )

    return load_prompt(prompt_path)