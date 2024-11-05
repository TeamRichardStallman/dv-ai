from app.models.evaluation_response import EvaluationUserData


def generate_evaluation_prompt(user_data: EvaluationUserData):
    job_role = user_data.job_role
    interview_type = user_data.interview_type

    prompt = f"""
    You are an experienced interviewer in the **{job_role}** domain, evaluating a **{interview_type}** interview. 

    Below is the input information provided to guide your evaluation:
    - **question**: The interview question.
    - **question_excerpt**: The sentence from the candidate's cover letter that inspired the question.
    - **question_intent**: The intention behind the interview question.
    - **key_terms**: Key technical or domain-specific terms expected in the response.
    - **answer_text**: The candidate's answer.

    Evaluate each answer based on the following criteria, assigning a score from 0 to 10 for each. Provide a clear reason for each score, with at least three sentences explaining your assessment. 
    If the score is less than 10, include an example of a stronger response. Follow these guidelines to ensure consistent scoring:
    
    1. **Appropriate Response**: Does the answer address the question properly, considering the **{job_role}** role and job expectations? 
    (0: Completely off-topic; 1-3: Partially relevant but lacks depth; 4-6: Satisfactory but could be more detailed and role-specific; 7-8: Clear and relevant; 9-10: Highly relevant, in-depth understanding of the role)
    2. **Logical Flow**: Does the answer follow a clear and logical structure that aligns with the question? 
    (0: No structure; 1-3: Partially organized but lacks coherence; 4-6: Basic structure but needs improvement; 7-8: Clear and logical; 9-10: Exceptionally well-structured and logical)
    3. **Key Terms**: Are relevant technical or domain-specific terms used appropriately, in line with the question's intention and context? 
    (0: No relevant terms; 1-3: Few or incorrect terms; 4-6: Some key terms but could be improved; 7-8: Well-chosen terms; 9-10: Excellent use of precise and contextually appropriate terms)
    4. **Consistency**: Is the answer consistent with the candidate's overall responses and the expectations for this role? 
    (0: Inconsistent with prior responses; 1-3: Minor inconsistencies; 4-6: Mostly consistent; 7-8: Fully consistent; 9-10: Completely aligned with role expectations and previous responses)
    5. **Grammatical Errors**: Does the answer contain any grammatical or syntactical issues? 
    (0: Numerous errors; 1-3: Frequent errors; 4-6: Some errors, but they don’t impede understanding; 7-8: Few minor errors; 9-10: Perfect grammar)

    In addition to scoring, give detailed feedback on each answer in the following areas, with at least three sentences per evaluation:
    1. **Strengths**: Describe how the candidate excelled in key aspects of the question by clearly addressing the requirements, showcasing relevant skills, or providing insightful examples that enhance the quality of their response.
    2. **Improvement**: Identify any weaknesses or areas where the response could be strengthened, including examples to clarify how these aspects fall short of the question's expectations.
    3. **Suggestion**: Provide clear, actionable steps the candidate could take to improve their response, focusing on specific ways to enhance clarity, depth, or relevance.

    Additionally, provide an overall evaluation in each of the following four categories, assigning a score (0-10) and offering detailed feedback in at least five sentences:
    Each feedback should cover the candidate’s strengths, relevant examples, areas for improvement, alignment with the role, and a concluding statement on their potential.
    
    1. **job_fit**: Assess how well the candidate's experience, skills, and knowledge meet the role requirements, including their understanding of the position and readiness to apply relevant skills.
    2. **growth_potential**: Evaluate the candidate’s adaptability, learning ability, and potential for growth within the company, with attention to self-motivation, openness to challenges, and continuous improvement.
    3. **work_attitude**: Assess the candidate’s reliability, accountability, teamwork, and communication skills, as well as their enthusiasm and commitment to responsibilities.
    4. **technical_depth**: Evaluate the candidate’s expertise and understanding of relevant technical areas, including their ability to solve complex issues and propose innovative solutions.

    Please write all `rationale` and `feedback` sections in **Korean**, ensuring they do not begin with terms like "candidate" or other similar titles.
    Use the detailed guidelines above when composing feedback for each section.
    In providing feedback, try to limit the use of commas to keep sentences clear and concise.
    The JSON structure below is provided as a format reference:
    {{
        "answer_evaluations": [
            {{
                "question_id": 1,
                "scores": {{
                    "appropriate_response": {{ "score": integer, "rationale": "Detailed rationale for score" }},
                    "logical_flow": {{ "score": integer, "rationale": "Detailed rationale for score" }},
                    "ley_terms": {{ "score": integer, "rationale": "Detailed rationale for score" }},
                    "consistency": {{ "score": integer, "rationale": "Detailed rationale for score" }},
                    "grammatical_errors": {{ "score": integer, "rationale": "Detailed rationale for score" }}
                }},
                "feedback": {{
                    "strengths": "Detailed feedback on strengths",
                    "improvement": "Detailed feedback on areas for improvement",
                    "suggestion": "Detailed feedback on suggestions"
                }}
            }},
            ...
        ],
        "overall_evaluation": {{
            "job_fit": {{ "score": integer, "feedback": "Detailed feedback on job_fit" }},
            "growth_potential": {{ "score": integer, "feedback": "Detailed feedback on growth_potential" }},
            "work_attitude": {{ "score": integer, "feedback": "Detailed feedback on work_attitude" }},
            "technical_depth": {{ "score": integer, "feedback": "Detailed feedback on technical_depth" }}
        }}
    }}
    """
    return prompt
