from langchain_core.prompts import PromptTemplate, load_prompt

from app.schemas.evaluation import EvaluationRequestModel

# Predefine the prompt mapping for clarity and efficiency
PROMPT_MAP = {
    ("chat", "real", "technical"): "app/prompts/chat/real_tech_chat_over.yaml",
    ("chat", "real", "personal"): "app/prompts/chat/real_personal_chat_over.yaml",
    ("chat", "general", "technical"): "app/prompts/chat/general_tech_chat_over.yaml",
    ("voice", "real", "technical"): "app/prompts/voice/real_tech_voice_over.yaml",
    ("voice", "real", "personal"): "app/prompts/voice/real_personal_voice_over.yaml",
    ("voice", "general", "technical"): "app/prompts/voice/general_tech_voice_over.yaml",
}


def generate_interview_evaluation_prompt(request_data: EvaluationRequestModel) -> PromptTemplate:
    key = (request_data.interview_method, request_data.interview_mode, request_data.interview_type)
    prompt_path = PROMPT_MAP.get(key)

    if not prompt_path:
        raise ValueError(
            f"Invalid combination of interview_method '{request_data.interview_method}', "
            f"interview_mode '{request_data.interview_mode}', "
            f"and interview_type '{request_data.interview_type}'"
        )

    return load_prompt(prompt_path)
