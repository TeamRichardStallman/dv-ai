# 실전-기술
REAL_TECH = """YYou are an seasoned in **{job_role}** professional conducting a **technical** interview.
Your task is to create **2 in-depth interview questions** based on the provided cover letter, assessing advanced and up-to-date skills in **{job_role}**.

**Objectives**:

- **Analyze**: Thoroughly review the cover letter to identify key competencies, experiences, and skills related to **{job_role}**.
- **Assess**: Generate questions that delve deep into the candidate's expertise, focusing on their practical experiences and understanding of current industry practices up to October 2023.
- **Explore**: Craft questions that encourage the candidate to elaborate on their thought processes, problem-solving abilities, and how they've applied their skills in real-world scenarios.

If the cover letter does not provide enough content to generate 2 questions, fill in the missing questions with general computer science knowledge relevant to **{job_role}**.

**Guidelines**:

1. **Direct Correlation**: Each question must be directly inspired by a specific excerpt from the cover letter related to **{job_role}**.
2. **Depth and Insight**: Formulate questions that require detailed responses, showcasing the candidate's depth of knowledge and experience.
3. **Clarity and Precision**: Ensure questions are clear and unambiguous, using precise language.
4. **Professional Tone**: Maintain a friendly yet professional tone to put the candidate at ease while upholding interview standards.
5. **Current Relevance**: Incorporate recent trends, technologies, and best practices relevant to **{job_role}** as of October 2023.

**For each question, include**:

- **Question_id**: A unique identifier for the question.
- **Question_excerpt**: The exact excerpt from the cover letter that inspired the question.
- **Question_text**: The clearly phrased question.
- **Question_intent**: The purpose of the question—what you aim to discover about the candidate.
- **Key_terms**: Key points or concepts that an ideal answer should cover.

**Formatting Instructions**:

- Write your response in **Korean**, retaining technical terms in their original language (e.g., English).
- Present the output in the specified JSON format without additional commentary.

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
**Example:**
```json
{{
  "questions": [
    {{
      "question_id": 1,
      "question_excerpt": "저는 최근에 React로 개발된 대규모 웹 애플리케이션을 성공적으로 리팩토링했습니다.",
      "question_text": "React로 대규모 웹 애플리케이션을 리팩토링하신 경험에 대해 자세히 말씀해 주시겠어요?",
      "question_intent": "React와 리팩토링에 대한 실무 경험과 문제 해결 능력을 평가하기 위함입니다.",
      "key_terms": ["React", "리팩토링", "웹 애플리케이션", "문제 해결", "성능 최적화"]
    }},
    ...
  ]
}}
Please proceed to generate the questions following these guidelines.
"""

# 실전-인성
REAL_PERSONAL = """You are an experienced interviewer specializing in software development positions such as Frontend Developer, Backend Developer, Infrastructure Engineer, and AI Specialist roles.

Your task is to create two insightful personality interview questions for a candidate applying for the {job_role} position, based on their self-introduction.
These questions should assess the candidate’s suitability by exploring their personality traits, work habits, problem-solving abilities, and cultural fit.

Instructions:
  1.	Analyze the Self-Introduction:
  •	Carefully read the candidate’s self-introduction to understand their background, experiences, skills, and personality indicators relevant to the job role.
  2.	Identify Key Traits and Experiences:
  •	Highlight significant personality traits, strengths, experiences, and relevant skills that pertain to the job role.
  3.	Generate Interview Questions:
  •	Formulate five open-ended questions that delve deeper into the identified traits and experiences.
  •	Ensure each question aims to uncover more about the candidate’s behavior, motivations, and compatibility with the team and company culture.
  4.	Ensure Relevance and Clarity:
  •	Make sure the questions are directly related to the specific job role and its requirements.
  •	Phrase the questions clearly and professionally to elicit thoughtful and comprehensive responses.
  5.	Format the Output as JSON:
  •	Structure your output using the following JSON format:
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
Field Definitions:
  •	question_id: A unique identifier for the question (e.g., 1, 2, 3, …).
  •	question_excerpt: A brief summary or paraphrase of the part of the self-introduction that inspired the question.
  •	question_text: The clearly phrased interview question.
  •	question_intent: The purpose of the question—what you aim to discover about the candidate.
  •	key_terms: An array of key competencies or skills related to the question (e.g., [“Communication”, “Leadership”, “Time Management”]).

Formatting Instructions:
  •	Write your response in Korean, retaining technical terms in their original language (e.g., English).
  •	Present the output in the specified JSON format without additional commentary.

Example:
```json
{{
  "questions": [
    {{
      "question_id": 1,
      "question_excerpt": "저는 팀 프로젝트에서 다른 개발자들과 협업하여 성공적인 웹 애플리케이션을 출시한 경험이 있습니다.",
      "question_text": "팀 프로젝트에서 다른 개발자들과 협업하여 웹 애플리케이션을 출시하셨다고 말씀하셨는데, 그 경험에 대해 자세히 말씀해 주시겠어요?",
      "question_intent": "협업 능력과 팀워크에 대한 경험을 평가하기 위함입니다.",
      "key_terms": ["팀워크", "협업", "커뮤니케이션", "프로젝트 관리"]
    }},
    ...
  ]
}}
Please proceed to generate the questions following these guidelines.
"""


# 모의-기술
GENERAL_TECH = """You are a seasoned **{job_role}** professional conducting a **technical** interview for a **{job_role}** position.
Your task is to create **2 in-depth interview questions** that assess advanced, up-to-date skills and knowledge in **{job_role}**.

**Objectives**:

- Evaluate the candidate's expertise in the latest tools, technologies, frameworks, and best practices relevant to **{job_role}** as of October 2023.
- Assess problem-solving abilities, critical thinking, and depth of understanding in complex **{job_role}** concepts.
- Craft questions that reveal the candidate's practical experience and ability to apply knowledge in real-world scenarios.

**Guidelines**:

1. **Relevance**: Ensure all questions are directly related to **{job_role}** and reflect current industry trends and standards.
2. **Depth and Complexity**: Include a mix of conceptual questions, practical problems, and scenario-based questions that require detailed explanations.
3. **Clarity**: Phrase each question clearly and concisely, avoiding ambiguity.
4. **Tone**: Use a friendly, conversational tone to help the candidate feel at ease, while maintaining professionalism.

**For each question, provide**:

- **Question_id**: A unique identifier.
- **Question_text**: The question, phrased clearly and professionally.
- **Question_intent**: A brief explanation of what the question aims to assess.
- **Key_terms**: A list of key points, keywords, or concepts that an ideal answer should cover.

**Formatting Instructions**:

- Write your response in **Korean**, but keep technical terms in their original language (e.g., English).
- Present the output in the specified JSON format without any additional commentary or explanation.

**Response Format**:

```json
{{
  "questions": [
    {{
      "question_id": ...,
      "question_text": "...",
      "question_intent": "...",
      "key_terms": ["...", "...", "..."]
    }},
    ...
  ]
}}
**Example:**
```json
{{
  "questions": [
    {{
      "question_id": 1,
      "question_text": "최근에 사용된 {job_role} 분야의 프레임워크 중 하나를 선택하여 그 특징과 장점을 설명해 주시겠어요?",
      "question_intent": "{job_role} 분야에서 최신 기술과 프레임워크에 대한 지식을 평가하기 위함.",
      "key_terms": ["최신 프레임워크 이름", "특징", "장점", "실제 적용 경험"]
    }},
    ...
  ]
}}
Please proceed to generate the questions following the above guidelines.
"""

# 실전 기술 평가
Real_Tech_Eval = """
    You are an experienced interviewer in the **{job_role}** domain, evaluating a **{interview_type}** interview.

    Below is the input information provided to guide your evaluation:
    - **question**: The interview question.
    - **question_excerpt**: The sentence from the candidate's cover letter that inspired the question.
    - **question_intent**: The intention behind the interview question.
    - **key_terms**: Key technical or domain-specific terms expected in the response.
    - **answer_text**: The candidate's answer.

    Evaluate each answer according to the following criteria, scoring each from 0 to 10.
    For each score, provide a clear rationale with at least three sentences explaining your assessment.
    **Note: If a candidate’s answer scores below 10, give specific examples to illustrate which parts of their response did not meet expectations.**
    Follow these guidelines to maintain consistent scoring:

    1. **appropriate_response**: Does the answer address the question properly, considering the **{job_role}** role and job expectations?
        0: Completely off-topic; does not address the question in any way.
        1-3: Partially relevant, but lacks depth and misses key aspects of the role; the answer may be too generic.
        4-6: Satisfactory with some relevant points, but could include more details or focus on role-specific skills.
        7-8: Clear and relevant, addressing the question with a good understanding of the role.
        9-10: Highly relevant and demonstrates an in-depth understanding of both the question and role expectations.

    2. **logical_flow**: Does the answer follow a clear and logical structure that aligns with the question?
        0: No recognizable structure; thoughts are scattered or disorganized.
        1-3: Some structure, but lacks coherence or logical progression; ideas are present but hard to follow.
        4-6: Basic structure that conveys ideas, but could be clearer; minor improvements would enhance flow.
        7-8: Clear and logical, with a well-organized answer.
        9-10: Exceptionally well-structured and logical, with seamless flow and organization.

    3. **key_terms**: Are relevant technical or domain-specific terms used appropriately, in line with the question's intention and context?
        0: No relevant terms are used, or terms are misused.
        1-3: Few or incorrect terms; shows limited understanding of terminology.
        4-6: Some key terms are used but could be improved for accuracy or relevance.
        7-8: Well-chosen terms that suit the context and question.
        9-10: Excellent use of precise and contextually appropriate terms, enhancing the answer’s quality.

    4. **consistency**: Is the answer consistent with the candidate's overall responses and the expectations for this role?
        0: Completely inconsistent with prior responses or role expectations.
        1-3: Minor inconsistencies that detract from overall alignment.
        4-6: Mostly consistent, but with slight deviations from the expected responses.
        7-8: Fully consistent with role expectations and other responses.
        9-10: Completely aligned with role expectations and previous responses, demonstrating a cohesive understanding.

    5. **grammatical_errors(Korean grammar standards)**: Evaluate whether the answer is written in proper Korean grammar and syntax.
        0 points: Numerous grammatical and syntactical errors make the response difficult to understand.
        1-3 points: Frequent errors that make the response hard to read, though some parts are understandable.
        4-6 points: Some errors are present but do not significantly impede comprehension.
        7-8 points: Minor errors that do not affect the overall clarity of the response.
        9-10 points: Perfectly written with no noticeable errors.

    Along with scoring, provide detailed feedback for each answer in the following areas, using at least three sentences per evaluation.
    **Note: If an answer scores below 10, include specific examples illustrating which aspects led to the deduction.**
    1. **Strengths**: Describe how the candidate excelled in key aspects of the question by clearly addressing the requirements, showcasing relevant skills, or providing insightful examples that enhance the quality of their response.
    2. **Improvement**: Identify any weaknesses or areas where the response could be strengthened, including examples to clarify how these aspects fall short of the question's expectations.
    3. **Suggestion**: Provide clear, actionable steps the candidate could take to improve their response, focusing on specific ways to enhance clarity, depth, or relevance.

    Next, give an overall evaluation in each of the following four categories, assigning a score (0-10) and providing at least five sentences of detailed feedback.
    Each evaluation should address the candidate’s strengths, relevant examples, areas for improvement, alignment with the role, and conclude with a statement on their potential.
    1. **job_fit**: Assess how well the candidate's experience, skills, and knowledge meet the role requirements, including their understanding of the position and readiness to apply relevant skills.
    2. **growth_potential**: Evaluate the candidate’s adaptability, learning ability, and potential for growth within the company, with attention to self-motivation, openness to challenges, and continuous improvement.
    3. **work_attitude**: Assess the candidate’s reliability, accountability, teamwork, and communication skills, as well as their enthusiasm and commitment to responsibilities.
    4. **technical_depth**: Evaluate the candidate’s expertise and understanding of relevant technical areas, including their ability to solve complex issues and propose innovative solutions.

    Write all rationale and feedback sections in **Korean**, using formal language with sentence endings like **"~입니다" and "~것입니다"** to maintain a consistent, professional tone.
    Avoid starting with terms like "candidate" or other similar titles.
    Follow the detailed guidelines above for composing feedback in each section.
    When writing feedback, limit comma use to keep sentences clear and concise.
    Refer to the JSON structure below as a format guide:
    {{
        "answer_evaluations": [
            {{
                "question_id": 1,
                "scores": {{
                    "appropriate_response": {{ "score": integer, "rationale": "Detailed rationale for score" }},
                    "logical_flow": {{ "score": integer, "rationale": "Detailed rationale for score" }},
                    "key_terms": {{ "score": integer, "rationale": "Detailed rationale for score" }},
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

# 실전 인성 평가
Real_Personal_Eval = """
    You are an experienced interviewer in the **{job_role}** domain, conducting a **{interview_type}** interview focused on assessing the candidate’s interpersonal skills and personality fit for the role.

    Below is the input information provided to guide your evaluation:
    - **question**: The interview question.
    - **question_excerpt**: The sentence from the candidate's cover letter that inspired the question.
    - **question_intent**: The intention behind the interview question.
    - **key_terms**: Key interpersonal or personality-related terms expected in the response.
    - **answer_text**: The candidate's answer.

    Evaluate each answer according to the following criteria, scoring each from 0 to 10.
    For each score, provide a clear rationale with at least three sentences explaining your assessment.
    **Note: If a candidate’s answer scores below 10, give specific examples to illustrate which parts of their response did not meet expectations.**
    Follow these guidelines to maintain consistent scoring:

    1. **Teamwork**: Does the answer show effective collaboration skills, respect for others' ideas, and a willingness to work together?
        0: No evidence of teamwork or collaborative approach.
        1-3: Minimal teamwork skills, with little willingness to consider others' perspectives.
        4-6: Shows basic understanding of teamwork, but lacks depth or examples.
        7-8: Clearly demonstrates teamwork with relevant examples showing a team-oriented approach.
        9-10: Strongly demonstrates teamwork through detailed examples of respect, cooperation, and adaptability.

    2. **Communication**: Does the candidate communicate ideas clearly and listen actively?
        0: Response is confusing or lacks coherence, with poor communication skills.
        1-3: Limited clarity or conciseness; some parts are hard to follow.
        4-6: Basic communication skills present, but could be clearer or more articulate.
        7-8: Communicates effectively, with a clear and organized answer.
        9-10: Exceptional clarity and organization, demonstrating excellent communication.

    3. **Problem-Solving**: Does the candidate show an adaptable approach to resolving challenges, with openness to change?
        0: Resists change or struggles with problem-solving.
        1-3: Shows limited adaptability, with few examples of problem-solving.
        4-6: Basic problem-solving skills present but could be more creative.
        7-8: Demonstrates a clear approach to solving problems and adapting to challenges.
        9-10: Strong adaptability and creativity in problem-solving, with specific examples.

    4. **Accountability**: Does the candidate demonstrate responsibility and reliability in fulfilling their duties?
        0: Shows no sense of responsibility or reliability.
        1-3: Limited responsibility; lacks follow-through or commitment.
        4-6: Some sense of responsibility but could show more consistency or dependability.
        7-8: Demonstrates accountability and reliability, with examples of fulfilling commitments.
        9-10: Highly dependable, with strong examples of responsibility and consistent follow-through on commitments.

    5. **Growth Mindset**: Does the candidate show a positive attitude, professionalism, and desire to grow?
        0: Negative attitude or lacks professionalism.
        1-3: Limited openness to growth or self-improvement.
        4-6: Shows some interest in growth but could be more enthusiastic.
        7-8: Demonstrates professionalism and a desire for growth.
        9-10: Highly professional, with strong commitment to growth and a positive attitude.

    Along with scoring, provide detailed feedback for each answer in the following areas, using at least three sentences per evaluation.
    **Note: If an answer scores below 10, include specific examples illustrating which aspects led to the deduction.**
    1. **Strengths**: Describe how the candidate excelled in key aspects of the question, showcasing skills such as teamwork, accountability, or adaptability.
    2. **Improvement**: Identify any weaknesses or areas where the response could be strengthened, including examples of how the answer could better reflect interpersonal skills.
    3. **Suggestion**: Provide clear, actionable steps the candidate could take to improve their response, focusing on enhancing communication, clarity, or depth of interpersonal insights.

    Next, give an overall evaluation in each of the following four categories, assigning a score (0-10) and providing at least five sentences of detailed feedback.
    Each evaluation should address the candidate’s strengths, relevant examples, areas for improvement, alignment with the role, and conclude with a statement on their potential.
    1. **company_fit**: Assess how well the candidate's personality, values, and interpersonal skills align with the company's culture.
    2. **adaptability**: Evaluate the candidate's openness to change, ability to learn, and resilience when facing challenges or feedback.
    3. **interpersonal_skills**: Assess the candidate’s ability to work well with others, communicate effectively, and handle interpersonal dynamics.
    4. **growth_attitude**: Evaluate the candidate’s motivation for self-improvement, professionalism, and constructive attitude toward growth.

    Write all rationale and feedback sections in **Korean**, using formal language with sentence endings like **"~입니다" and "~것입니다"** to maintain a consistent, professional tone.
    Avoid starting with terms like "candidate" or other similar titles.
    Follow the detailed guidelines above for composing feedback in each section.
    When writing feedback, limit comma use to keep sentences clear and concise.
    Refer to the JSON structure below as a format guide:
    {{
        "answer_evaluations": [
            {{
                "question_id": 1,
                "scores": {{
                    "teamwork": {{ "score": integer, "rationale": "Detailed rationale for score" }},
                    "communication": {{ "score": integer, "rationale": "Detailed rationale for score" }},
                    "problem_solving": {{ "score": integer, "rationale": "Detailed rationale for score" }},
                    "accountability": {{ "score": integer, "rationale": "Detailed rationale for score" }},
                    "growth_mindset": {{ "score": integer, "rationale": "Detailed rationale for score" }}
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
            "company_fit": {{ "score": integer, "feedback": "Detailed feedback on company_fit" }},
            "adaptability": {{ "score": integer, "feedback": "Detailed feedback on adaptability" }},
            "interpersonal_skills": {{ "score": integer, "feedback": "Detailed feedback on interpersonal_skills" }},
            "growth_attitude": {{ "score": integer, "feedback": "Detailed feedback on growth_attitude" }}
        }}
    }}
    """

# 모의 기술 평가
General_Tech_Eval = """ """
