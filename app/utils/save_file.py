import json
import os
import logging
from datetime import datetime
from app.utils.logger import setup_logger, get_logger

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "../logs/ai_results")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

log_file_path = os.path.join(LOG_DIR, "app.log")
setup_logger(log_level=logging.INFO, log_file=log_file_path)


def save_prompt_and_result(prompt, model_input, result):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"result_{timestamp}.json"
    file_path = os.path.join(LOG_DIR, file_name)

    data = {"timestamp": timestamp, "prompt": prompt, "model_input": model_input, "result": result}

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    logger = get_logger()
    logger.info(f"Prompt and result saved to {file_path}")
    print(f"Data saved to {file_path}")
