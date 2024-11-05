from app.models.questions_response import QusetionsRequest


def generate_questions_prompt(user_data: QusetionsRequest):
    job_role = user_data.job_role
    interview_type = user_data.interview_type

    prompt = f"""
You are an seasoned in **{job_role}** professional conducting a **{interview_type}** interview.
Your task is to create **10 in-depth interview questions** based on the provided cover letter, assessing advanced and up-to-date skills in **{job_role}**.

**Objectives**:

- **Analyze**: Thoroughly review the cover letter to identify key competencies, experiences, and skills related to **{job_role}**.
- **Assess**: Generate questions that delve deep into the candidate's expertise, focusing on their practical experiences and understanding of current industry practices up to October 2023.
- **Explore**: Craft questions that encourage the candidate to elaborate on their thought processes, problem-solving abilities, and how they've applied their skills in real-world scenarios.

    If the cover letter does not provide enough content to generate 10 questions, fill in the missing questions with general computer science knowledge relevant to **{job_role}**.

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
    return prompt

def generate_questions_prompt_general(user_data: dict):
    job_role = user_data.get("job_role")
    interview_type = user_data.get("interview_type")
    
    prompt = f"""
You are a seasoned **{job_role}** professional conducting a **{interview_type}** interview for a **{job_role}** position.
Your task is to create **10 in-depth interview questions** that assess advanced, up-to-date skills and knowledge in **{job_role}**.

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

- **Question_id**: A unique identifier (e.g., Q1, Q2, ..., Q10).
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
    return prompt
