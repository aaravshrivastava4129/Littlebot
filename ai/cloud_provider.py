from openai import (
    OpenAI,
    APIConnectionError,
    APIStatusError,
    AuthenticationError,
    RateLimitError,
)

from ai.provider import AIProvider
from config.settings import (
    CLOUDFLARE_API_TOKEN,
    CLOUDFLARE_BASE_URL,
    LLAMA_MODEL,
    TEMPERATURE,
    MAX_RESPONSE_TOKENS,
)


class CloudLlamaProvider(AIProvider):

    def __init__(self):

        if not CLOUDFLARE_API_TOKEN:
            raise ValueError(
                "Cloudflare API token is missing."
            )

        self.client = OpenAI(
            api_key=CLOUDFLARE_API_TOKEN,
            base_url=CLOUDFLARE_BASE_URL,
        )

        self.model = LLAMA_MODEL

    def reply(self, messages: list[dict[str, str]]) -> str:

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=TEMPERATURE,
                max_tokens=MAX_RESPONSE_TOKENS,
            )

            content = response.choices[0].message.content

            return content or "I couldn't generate a response."

        except AuthenticationError:
            return "My AI credentials are invalid."

        except RateLimitError:
            return "I've reached my AI usage limit. Please try later."

        except APIConnectionError:
            return "I can't connect to my AI service right now."

        except APIStatusError as error:
            return f"My AI service returned an error: {error.status_code}"
