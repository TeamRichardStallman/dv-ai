import os
import weave
from app.models.questions_response import QuestionsRequest

weave.init('ticani0610-no/weave-trace')

_prompt_cache = {}

# Get the current directory once at module load time
_current_dir = os.path.dirname(os.path.abspath(__file__))

def generate_questions_prompt(user_data: QuestionsRequest):
    try:
        job_role = user_data.job_role
        interview_type = user_data.interview_type
        interview_mode = user_data.interview_mode
    except KeyError as e:
        raise KeyError(f"Missing required key in user_data: {e}")

    if interview_mode == 'real':
        filename = 'real-tech.txt' if interview_type == 'technical' else 'real-personal.txt'
    elif interview_mode == 'general':
        filename = 'general-tech.txt'

    file_path = os.path.join(_current_dir, filename)

    generation_prompt = _prompt_cache.get(file_path)
    if generation_prompt is None:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Cannot find the file: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as file:
            generation_prompt = file.read()
            _prompt_cache[file_path] = generation_prompt

    weave.publish(obj=generation_prompt, name=f"{interview_mode}-{interview_type}")

    try:
        prompt = generation_prompt.format(job_role=job_role, interview_type=interview_type)
    except KeyError as e:
        raise KeyError(f"Missing key during prompt formatting: {e}")

    return prompt
