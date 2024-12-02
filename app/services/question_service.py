import weave

from app.prompts.question import GENERAL_TECH, REAL_PERSONAL, REAL_TECH
from app.schemas.question import QuestionsRequest

weave.init("ticani0610-no/prompt-test")


def generate_questions_prompt(interview_id: int, user_data: QuestionsRequest):
    try:
        user_id = user_data.user_id
        job_role = user_data.job_role
        interview_type = user_data.interview_type
        interview_mode = user_data.interview_mode
        question_count = user_data.question_count
    except KeyError as e:
        raise KeyError(f"Missing required key in user_data: {e}")

    if interview_mode == "real":
        if interview_type == "technical":
            generation_prompt = REAL_TECH
        elif interview_type == "personal":
            generation_prompt = REAL_PERSONAL
    elif interview_mode == "general":
        generation_prompt = GENERAL_TECH
    else:
        raise ValueError(f"Unknown interview_mode: {interview_mode}")

    weave.publish(obj=generation_prompt, name=f"prompt: {interview_mode}-{interview_type}")

    try:
        prompt = generation_prompt.format(
            job_role=job_role, question_count=question_count, user_id=user_id, interview_id=interview_id
        )
    except KeyError as e:
        raise KeyError(f"Missing key during prompt formatting: {e}")

    return prompt
