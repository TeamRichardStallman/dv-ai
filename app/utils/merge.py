from app.schemas.evaluation import AnswerResponse
from app.schemas.question import QuestionsResponse


def merge_questions_and_answers(questions: QuestionsResponse, answers: AnswerResponse):
    merged_data = []

    for q in questions.questions:
        answer = next(
            (a for a in answers.answers if a.question_id == q.question_id),
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
                    "answer_text": answer.answer_text,
                }
            )
    return merged_data
