"""Simple LLM inference helpers."""

from openai import OpenAI

from utils.config import settings

Message = dict[str, str]


def _client() -> OpenAI:
    return OpenAI(
        api_key=settings.llm_api_key,
        base_url=settings.llm_base_url,
    )


def chat_completion(
    messages: list[Message],
    temperature: float = 0.0,
    max_tokens: int = 4096,
    verbose: bool = False,
) -> str | dict[str, str | None]:
    
    response = _client().chat.completions.create(
        model=settings.llm_model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    message = response.choices[0].message
    content = message.content.strip() if message.content else ""

    reasoning_content = getattr(message, "reasoning_content", None)
    provider_fields = getattr(message, "provider_specific_fields", None) or {}
    if reasoning_content is None:
        reasoning_content = provider_fields.get("reasoning_content")
    if reasoning_content is None:
        reasoning_content = provider_fields.get("reasoning")

    if verbose:
        return {
            "content": content,
            "reasoning_content": reasoning_content.strip() if reasoning_content else None,
        }

    return content


def inference(
    prompt: str,
    system_prompt: str | None = None,
    temperature: float = 0.0,
    max_tokens: int = 4096,
    verbose: bool = False,
) -> str | dict[str, str | None]:
    messages: list[Message] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    return chat_completion(
        messages,
        temperature=temperature,
        max_tokens=max_tokens,
        verbose=verbose,
    )
