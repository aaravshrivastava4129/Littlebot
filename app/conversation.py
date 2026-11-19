from app.personality import SYSTEM_PROMPT
from config.settings import MAX_HISTORY_MESSAGES
from ai.factory import get_ai_provider

class Conversation:
    def __init__(self):
        self.provider = get_ai_provider()

        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    def send_message(self, user_message: str) -> str:

        self.messages.append({"role": "user", "content" : user_message})

        response = self.provider.reply(self.messages)

        self.messages.append({"role": "assistant", "content": response})

        self._manage_history()

        return response

    def _manage_history(self):
        recent_messages = self.messages[1:]

        self.messages = [self.messages[0]] + recent_messages[ - MAX_HISTORY_MESSAGES:]