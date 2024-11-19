from app.schemas.evaluation import AnswerResponse
from app.schemas.question import QuestionsResponse


def merge_questions_and_answers(questions: QuestionsResponse, answers: AnswerResponse):
    merged_data = []

    for question in questions.questions:
        answer = next(
            (a for a in answers.answers if a.question_id == question.question_id),
            None,
        )
        if answer:
            merged_data.append(
                {
                    "question_id": question.question_id,
                    "question_excerpt": question.question_excerpt,
                    "question_text": question.question_text,
                    "question_intent": question.question_intent,
                    "key_terms": question.key_terms,
                    "answer_text": answer.answer_text,
                }
            )
    return merged_data
