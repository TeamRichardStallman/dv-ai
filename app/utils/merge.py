def merge_questions_answers(questions, answers):
    merged_data = []
    for question in questions["questions"]:
        answer = next((a for a in answers["answers"] if a["question_id"] == question["question_id"]), None)
        if answer:
            merged_data.append({
                "question_id": question["question_id"],
                "question_text": question["question_text"],
                "answer_text": answer["answer_text"]
            })
    return merged_data