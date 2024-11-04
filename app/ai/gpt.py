from openai import OpenAI
import json
from app.config import Config
from typing import Any
import time
import hashlib
import wandb
from wandb.sdk.data_types.trace_tree import Trace
from typing import Literal

client_gpt = OpenAI(api_key=Config.OPENAI_API_KEY)


def generate_run_id(prompt: str, input: str):
    run_str = prompt + input
    return hashlib.md5(run_str.encode("utf-8")).hexdigest()


# W&B login
wandb.login(key=Config.WANDB_API_KEY)


def generate_from_gpt(prompt: str, input: str, type: Literal["question", "evaluation"]) -> Any:
    run_id = generate_run_id(prompt, input)
    # Initialize W&B only if not already initialized
    if wandb.run is None:
        wandb.init(project="dev_ai", name=f"{type}_prompt", id=run_id, resume="allow")

    start_time = time.time()

    # Define the cost per 1K tokens
    COST_PER_1K_TOKENS = 0.002

    try:
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
        token_usage = response.usage.to_dict()
        total_tokens = token_usage.get("total_tokens", 0)
        usage_fee = (total_tokens / 1000) * COST_PER_1K_TOKENS
        status_code = "success"
        status_message = ""

    except Exception as e:
        response_content = ""
        token_usage = {}
        total_tokens = 0
        usage_fee = 0.0
        status_code = "error"
        status_message = str(e)
        raise

    finally:
        end_time = time.time()
        gen_time = end_time - start_time

        # Create Trace object
        root_span = Trace(
            name="root_span",
            kind="llm",
            status_code=status_code,
            status_message=status_message,
            metadata={
                "temperature": Config.TEMPERATURE,
                "model_name": Config.GPT_MODEL,
                "gen_time": f"{gen_time:.2f} seconds",
                "token_usage": token_usage,
                "usage_fee": f"${usage_fee:.6f}",
            },
            start_time_ms=int(start_time * 1000),
            end_time_ms=int(end_time * 1000),
            inputs={"system_prompt": prompt, "input": input},
            outputs={"response": response_content} if response_content else {},
        )

        root_span.log(name="dev_ai")

        wandb.finish()

    return json.loads(response_content)
