import json
from typing import Literal, Union
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

# import weave
from openai import OpenAI

# import wandb
from app.core.config import Config
from app.schemas.evaluation import EvaluationRequest, PersonalEvaluationResponse, TechnicalEvaluationResponse
from app.schemas.question import QuestionsRequest, QuestionsResponse

client_gpt = OpenAI(api_key=Config.OPENAI_API_KEY)
chroma_client = chromadb.Client()

openai_ef = OpenAIEmbeddingFunction(
    api_key=Config.OPENAI_API_KEY,
    model_name="text-embedding-3-small"
)

# W&B login
# wandb.login(key=Config.WANDB_API_KEY)

# weave.init("ticani0610-no/prompt-test")


class ContentGenerator:
    cache = {}
    semantic_cache = chroma_client.create_collection(name="semantic_cache",
        embedding_function=openai_ef,
        metadata={"hnsw:space": "cosine"}
    )

    def __init__(self, user_data: Union[QuestionsRequest, EvaluationRequest]):
        self.user_data = user_data

    # @weave.op(call_display_name=lambda call: f"{call.func_name}__{datetime.now()}")
    def invoke(self, prompt: str, input: str, choice: Literal["question", "evaluation"]):
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
            # weave.publish(weave.Dataset(name="dataset", rows=[{"cover_letter": input}]))
            return QuestionsResponse(**parsed_content)
        elif choice == "evaluation":
            if self.user_data.interview_type == "technical":
                return TechnicalEvaluationResponse(**parsed_content)
            elif self.user_data.interview_type == "personal":
                return PersonalEvaluationResponse(**parsed_content)
