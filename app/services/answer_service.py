from langchain_core.prompts import PromptTemplate, load_prompt

from app.schemas.answer import AnswerRequestModel
from app.services.s3_service import S3Service
from app.services.stt_service import STTService
from app.utils.format import clean_text


async def generate_answer_evaluation_new_request_data(
    request_data: AnswerRequestModel,
    s3_service: S3Service,
    stt_service: STTService,
):
    new_requset_data = request_data
    if new_requset_data.interview_method == "chat":
        return new_requset_data, 1

    if new_requset_data.interview_method != "chat":
        s3_audio_url = new_requset_data.answer.s3_audio_url
        if not s3_audio_url:
            raise ValueError("s3_audio_url is required")
        audio_file = await s3_service.get_s3_object(s3_audio_url)
        transcribed_text, wpm = await stt_service.transcribe_audio(audio_file)
        cleaned_text = clean_text(transcribed_text)
        answer_text = cleaned_text
        new_requset_data.answer.answer_text = answer_text
        return new_requset_data, wpm


# Predefine the prompt mapping for clarity and efficiency
PROMPT_MAP = {
    ("chat", "real", "technical"): "app/prompts/chat/real_tech_chat_eval.yaml",
    ("chat", "real", "personal"): "app/prompts/chat/real_personal_chat_eval.yaml",
    ("chat", "general", "technical"): "app/prompts/chat/general_tech_chat_eval.yaml",
    ("voice", "real", "technical"): "app/prompts/voice/real_tech_voice_eval.yaml",
    ("voice", "real", "personal"): "app/prompts/voice/real_personal_voice_eval.yaml",
    ("voice", "general", "technical"): "app/prompts/voice/general_tech_voice_eval.yaml",
}


async def generate_answer_evaluation_prompt(request_data: AnswerRequestModel) -> PromptTemplate:
    key = (request_data.interview_method, request_data.interview_mode, request_data.interview_type)
    prompt_path = PROMPT_MAP.get(key)

    if not prompt_path:
        raise ValueError(
            f"Invalid combination of interview_method '{request_data.interview_method}', "
            f"interview_mode '{request_data.interview_mode}', "
            f"and interview_type '{request_data.interview_type}'"
        )

    return load_prompt(prompt_path)
