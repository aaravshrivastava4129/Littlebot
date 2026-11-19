from abc import ABC, abstractmethod

class AIProvider(ABC):

    @abstractmethod
    def reply(self, messages: list[dict[str, str]]) -> str:
        """
        Generate an AI response from conversation history.
        """
        pass