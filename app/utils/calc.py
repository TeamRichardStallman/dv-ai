from typing import List

import tiktoken
from openai import OpenAI

from app.core.config import Config

client_gpt = OpenAI(api_key=Config.OPENAI_API_KEY)


def count_tokens(text: str, model: str = "gpt-4") -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def split_text_by_tokens(text: str, max_tokens: int, model: str = "gpt-4") -> List[str]:
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    chunks = [tokens[i : i + max_tokens] for i in range(0, len(tokens), max_tokens)]
    return [encoding.decode(chunk) for chunk in chunks]


def split_text_by_paragraphs(text: str, max_tokens: int, model: str = "gpt-4") -> List[str]:
    paragraphs = text.split("\n\n")
    current_chunk = []
    current_tokens = 0
    encoding = tiktoken.encoding_for_model(model)
    chunks = []

    for paragraph in paragraphs:
        paragraph_tokens = len(encoding.encode(paragraph))
        if current_tokens + paragraph_tokens > max_tokens:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = []
            current_tokens = 0
        current_chunk.append(paragraph)
        current_tokens += paragraph_tokens

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks


def process_chunks_with_gpt(chunks: List[str], model: str = "gpt-4", max_tokens: int = 50000) -> List[str]:
    responses = []
    for chunk in chunks:
        response = client_gpt.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": chunk}],
            max_tokens=max_tokens,
        )
        response_content = response.choices[0].message.content

        responses.append(response_content)
    return responses


def summarize_large_text(text: str, model: str = "gpt-4", max_tokens: int = 50000) -> str:
    chunks = split_text_by_tokens(text, max_tokens=max_tokens, model=model)
    summaries = process_chunks_with_gpt(chunks, model=model, max_tokens=2000)
    combined_summary = " ".join(summaries)
    final_summary = process_chunks_with_gpt([combined_summary], model=model, max_tokens=2000)
    return final_summary[0]
