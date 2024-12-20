from app.prompts.chat.chat_evaluation import GENERAL_TECH_CHAT_EVAL, REAL_PERSONAL_CHAT_EVAL, REAL_TECH_CHAT_EVAL
from app.prompts.voice.voice_evaluation import GENERAL_TECH_VOICE_EVAL, REAL_PERSONAL_VOICE_EVAL, REAL_TECH_VOICE_EVAL
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


async def generate_answer_evaluation_prompt(
    interview_id: int,
    request_data: AnswerRequestModel,
    wpm: float,
) -> str:
    user_id = request_data.user_id
    question_id = request_data.question.question_id
    job_role = request_data.job_role
    interview_type = request_data.interview_type
    interview_mode = request_data.interview_mode
    interview_method = request_data.interview_method
    s3_audio_url = request_data.answer.s3_audio_url
    s3_video_url = request_data.answer.s3_video_url

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
            interview_id=interview_id,
            question_id=question_id,
            job_role=job_role,
            interview_type=interview_type,
            wpm=wpm,
            s3_audio_url=s3_audio_url,
            s3_video_url=s3_video_url,
        )
    except KeyError as e:
        raise KeyError(f"Missing key during prompt formatting: {e}")

    return prompt
