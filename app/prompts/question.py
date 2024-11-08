from app.models.questions_response import QuestionsRequest


def generate_questions_prompt(user_data: QuestionsRequest):
    job_role = user_data.job_role
    interview_type = user_data.interview_type

    prompt = f"""
    You are an expert in **{job_role}** and will be conducting a **{interview_type}** interview.
    Your task is to create **10 interview questions** based on the provided cover letter.

    If the cover letter does not provide enough content to generate 10 questions, fill in the missing questions with general computer science knowledge relevant to **{job_role}**.

    **Guidelines**:

    1. Carefully analyze the key competencies and experiences highlighted in the cover letter, considering the applied job role.
    2. Generate questions based on the applicant's described experiences, focusing on their thought processes and problem-solving abilities.
    3. Note any grammatical errors or out-of-context word usage, especially in relation to the job role.
    4. Ensure questions reflect the core competencies of the candidate, avoiding abstract concepts to facilitate evaluation.
    5. Phrase the questions in a friendly, conversational tone to help the candidate relax, while maintaining an undertone of professionalism.

    **For each question, include**:

    - **Question_id**: Unique identifier for the question.
    - **Excerpt**: The exact excerpt from the cover letter that inspired the question.
    - **Question**: The question itself, phrased clearly and professionally.
    - **Intention**: The purpose behind the question—what you aim to discover about the candidate.
    - **Key Points**: Key points or keywords that should be included in an ideal answer.

    **Instructions**:

    - Write your response in **Korean**, but retain technical terms in their original language (e.g., English).
    - Ensure the questions are directly related to the applicant's experiences, achievements, and skills mentioned in the cover letter.
    - Focus on creating questions that require the candidate to elaborate on their experiences, thought processes, and problem-solving abilities.

    **Response Format**:

    ```json
    {{
      "questions": [
        {{
          "question_id": ...,
          "question_excerpt": ...,
          "question_text": ...,
          "question_intent": ...,
          "key_terms": ["competency1", "competency2", "competency3"]
        }},
        ...
      ]
    }}
    """
    return prompt
