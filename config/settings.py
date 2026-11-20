import os
from dotenv import load_dotenv

load_dotenv()

AI_PROVIDER = os.getenv("AI_PROVIDER", "cloudflare").lower()

CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")

if not CLOUDFLARE_ACCOUNT_ID:
    raise ValueError("Cloudflare Account ID is missing.")

CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")

if not CLOUDFLARE_API_TOKEN:
    raise ValueError("Cloudflare API token is missing.")

CLOUDFLARE_BASE_URL = (f"https://api.cloudflare.com/client/v4/accounts/"f"{CLOUDFLARE_ACCOUNT_ID}/ai/v1")

LLAMA_MODEL = "@cf/google/gemma-4-26b-a4b-it"

MAX_HISTORY_MESSAGES = 20
TEMPERATURE = 0.7
MAX_RESPONSE_TOKENS = 1024

AUDIO_SAMPLE_RATE = 16000
AUDIO_CHANNELS = 1
AUDIO_DTYPE = "float32"