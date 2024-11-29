import json
from typing import Literal, Union
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

from openai import OpenAI

from app.core.config import Config
from app.schemas.answer import AnswerResponseModel
from app.schemas.evaluation import (
    EvaluationRequestModel,
    PersonalEvaluationResponseModel,
    TechnicalEvaluationResponseModel,
)
from app.schemas.question import QuestionsRequestModel, QuestionsResponseModel
from app.utils.generate import ensure_feedback_fields

client_gpt = OpenAI(api_key=Config.OPENAI_API_KEY)
chroma_client = chromadb.Client()

openai_ef = OpenAIEmbeddingFunction(
    api_key=Config.OPENAI_API_KEY,
    model_name="text-embedding-3-small"
)


class ContentGenerator:
    cache = {}
    semantic_cache = chroma_client.create_collection(name="semantic_cache",
        embedding_function=openai_ef,
        metadata={"hnsw:space": "cosine"}
    )

    def __init__(self, request_data: Union[QuestionsRequestModel, EvaluationRequestModel]):
        self.request_data = request_data

    def invoke(self, prompt: str, input: str, choice: Literal["question", "answer", "evaluation"]):
        cache_key = f"{prompt}|{input}"

        if cache_key not in self.cache:
            similar_doc = self.semantic_cache.query(query_texts=[cache_key], n_results=1)
            if (similar_doc["documents"] and similar_doc["documents"][0] and similar_doc["distances"][0][0] < 0.2):
                cached_metadata = similar_doc["metadatas"][0][0]
                response_content = cached_metadata["response"]
                self.cache[cache_key] = response_content
            else:
                response = client_gpt.chat.completions.create(
                    model=Config.GPT_MODEL,
                    messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": input},
                    ],
                    response_format={"type": "json_object"},
                    seed=Config.SEED,
                    temperature=Config.TEMPERATURE,
                    top_p=Config.TOP_P,
            )

                response_content = response.choices[0].message.content
                self.cache[cache_key] = response_content
                self.semantic_cache.add(documents=[cache_key], metadatas=[{"response": response_content}], ids=[cache_key])

        parsed_content = json.loads(self.cache[cache_key])

        if choice == "question":
            return QuestionsResponseModel(**parsed_content)
        elif choice == "answer":
            parsed_content = ensure_feedback_fields(parsed_content)
            return AnswerResponseModel(**parsed_content)
        elif choice == "evaluation":
            if self.request_data.interview_type == "technical":
                return TechnicalEvaluationResponseModel(**parsed_content)
            elif self.request_data.interview_type == "personal":
                return PersonalEvaluationResponseModel(**parsed_content)
