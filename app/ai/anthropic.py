import anthropic
from app.core.config import Config

client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)


def generate_from_anthropic(system: str, input: str):
    message = (
        client.messages.create(
            model=Config.ANTHROPIC_MODEL,
            max_tokens=8192,
            temperature=Config.TEMPERATURE,
            top_p=Config.TOP_P,
            system=system,
            messages=[{"role": "user", "content": input}],
        )
        .content[0]
        .text
    )

    return message
