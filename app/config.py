import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    GPT_MODEL = "gpt-3.5-turbo"  # 테스트용. 프롬프팅 성능 테스트 후 gpt-4o로 변경하기
    # GPT_MODEL = "gpt-4o"
    ANTHROPIC_MODEL = "claude-3-opus-20240229"
    
    SEED = 456  # 동일한 입력에 대해 일관된 결과를 생성
    TEMPERATURE = 0.78  # 적당히 창의적이고 예측할 수 없는 출력
    TOP_P = 0.8  # 적당히 다양한 단어를 포함, 가능성 높은 후보군을 중심으로 선택