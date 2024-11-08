import weave
from app.models.questions_response import QuestionsRequest
from app.prompts.prompt import REAL_TECH, REAL_PERSONAL, GENERAL_TECH

weave.init('ticani0610-no/prompt-test')

def generate_questions_prompt(user_data: QuestionsRequest):
    try:
        job_role = user_data.job_role
        interview_type = user_data.interview_type
        interview_mode = user_data.interview_mode
    except KeyError as e:
        raise KeyError(f"Missing required key in user_data: {e}")

    # 프롬프트 변수를 직접 매핑하여 사용
    if interview_mode == 'real':
        if interview_type == 'technical':
            generation_prompt = REAL_TECH
        elif interview_type == 'personal':
            generation_prompt = REAL_PERSONAL
    elif interview_mode == 'general':
        generation_prompt = GENERAL_TECH
    else:
        raise ValueError(f"Unknown interview_mode: {interview_mode}")

    weave.publish(obj=generation_prompt, name=f"prompt: {interview_mode}-{interview_type}")

    try:
        prompt = generation_prompt.format(job_role=job_role)
    except KeyError as e:
        raise KeyError(f"Missing key during prompt formatting: {e}")

    return prompt