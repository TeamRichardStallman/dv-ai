from typing import List

from app.schemas.evaluation import SimplifiedAnswerResponse
from app.schemas.question import QuestionsResponse, Question
from app.schemas.answer import AnswerModel


def merge_questions_and_answers(questions: QuestionsResponse, answers: List[SimplifiedAnswerResponse]):
    merged_data = []

    for q in questions.questions:
        answer = next(
            (a for a in answers if a.question_id == q.question_id),
            None,
        )
        if answer:
            merged_data.append(
                {
                    "question_id": q.question_id,
                    "question_excerpt": q.question_excerpt,
                    "question": {
                        "question_text": q.question.question_text,
                        "s3_audio_url": q.question.s3_audio_url,
                        "s3_video_url": q.question.s3_video_url,
                    },
                    "question_intent": q.question_intent,
                    "key_terms": q.key_terms,
                    "answer_text": answer.answer.answer_text,
                }
            )
    return merged_data


def merge_question_and_answer(question: Question, answer: AnswerModel) -> dict:
    return {
        "question_id": question.question_id,
        "question_excerpt": question.question_excerpt,
        "question": {
            "question_text": question.question.question_text,
            "s3_audio_url": question.question.s3_audio_url,
            "s3_video_url": question.question.s3_video_url,
        },
        "question_intent": question.question_intent,
        "key_terms": question.key_terms,
        "answer_text": answer.answer_text,
    }
