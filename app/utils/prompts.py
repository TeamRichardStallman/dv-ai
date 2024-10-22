def generate_questions_prompt(user_data):
    job_role = user_data.get("job_role")
    interview_focus = user_data.get("interview_focus")
    language = user_data.get("language", "ko")  # 기본 언어는 영어로 설정

    language_note = f"Please provide the questions in {language}." if language != "ko" else ""

    prompt = f"""
    You are an expert in the {job_role} domain and the interviewer for a {interview_focus} interview.
    Your task is to create 10 interview questions based on the provided cover letter for a {interview_focus} interview.
    If the cover letter does not provide enough content to generate 10 questions, fill in the missing questions with general CS knowledge questions relevant to {job_role}.

    {language_note}

    Process:
    Follow these guidelines when generating interview questions:
    1. Carefully analyze the key competencies the candidate is trying to appeal to, taking into account the job applied for and the context.
    2. Try to generate questions based on the experiences described by the applicant.
    3. Grammatical errors and out-of-context word usage should be analyzed with some degree of refinement in light of the job applied for.
    4. When creating questions, be sure to consider the core competencies of the candidate you are trying to capture. Core competencies should not be abstract to make it easier to evaluate answers.
    5. The questions should be phrased in a soft colloquial tone to help the candidate relax, but at the same time, the interviewer's sharpness should come through.

    Format:
    Present the results with JSON format with the following structure:
    {{
      "questions": [
        {{
          "question_id": Unique identifier for the question,
          "question_text": The text of the interview question,
          "question_intent": The purpose or intent of the question,
          "core_competency": ["competency1", "competency2", "competency3"],  # List of core competencies
          "model_answer": A model or ideal answer to the question
        }}
        ...
      ]
    }}
    """

    return prompt

def generate_evaluation_prompt(user_data):
    job_role = user_data.get("job_role")
    interview_focus = user_data.get("interview_focus")
    language = user_data.get("language", "ko")

    language_note = f"Please provide all feedback in {language}." if language != "en" else ""

    prompt = f"""
    You are an experienced interviewer in the {job_role} domain, evaluating a {interview_focus} interview.
    Below are the interview questions and the candidate's answers. Evaluate each answer based on the following criteria:

    - Appropriate Response: Does the answer address the question properly?
    - Logical Flow: Does the answer follow a clear and logical structure?
    - Key Terms: Are relevant technical or domain-specific terms used appropriately?
    - Consistency: Is the answer consistent with the candidate's overall responses and role expectations?
    - Grammatical Errors: Does the answer contain any grammatical or syntactical issues?

    Ensure that all feedback is written in {language}.

    For each answer, provide a score (0-10) and a brief feedback explaining your evaluation.

    {language_note}

    Interview Data:
    user input

    Format your response as follows:
    {{
      "answer_evaluations": [
        {{
          "question_id": 1,
          "score": integer,  # 0 to 10
          "feedback_text": "text"  # Feedback in {language}
        }},
        {{
          "question_id": 2,
          "score": integer,  # 0 to 10
          "feedback_text": "text"  # Feedback in {language}
        }},
        ...
      ],
      "overall_evaluation": {{
        "development_skill": {{
          "score": integer,  # 0 to 10
          "feedback_text": "text"  # Feedback in {language}
        }},
        "growth_potential": {{
          "score": integer,  # 0 to 10
          "feedback_text": "text"  # Feedback in {language}
        }},
        "work_attitude": {{
          "score": integer,  # 0 to 10
          "feedback_text": "text"  # Feedback in {language}
        }},
        "technical_depth": {{
          "score": integer,  # 0 to 10
          "feedback_text": "text"  # Feedback in {language}
        }}
      }}
    }}
    """

    return prompt