def calculate_wpm(word_data: dict):
    # 총 단어 수 계산
    total_words = len(word_data.get("words"))
    if total_words == 0:
        return 0

    # 총 시간(초) 계산
    if word_data.get("duration") <= 0:
        return 0

    total_time_minutes = word_data.get("duration") / 60

    wpm = total_words / total_time_minutes

    return wpm
