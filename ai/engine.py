from ai.prompts import build_prompt
from ai.providers.provider_manager import ProviderManager


class AIEngine:

    def __init__(self):

        self.provider_manager = ProviderManager()

    def ask(

        self,

        message,

        system_prompt=""

    ):

        provider = self.provider_manager.default()

        if provider is None:

            return (
                "❌ No AI Provider Found.\n\n"
                "Please configure your API keys."
            )

        prompt = build_prompt(message)

        if provider == "gemini":

            from ai.providers.gemini_provider import ask_gemini

            return ask_gemini(

                prompt=prompt,

                system_prompt=system_prompt

            )

        if provider == "openai":

            from ai.providers.openai_provider import ask_openai

            return ask_openai(

                prompt=prompt,

                system_prompt=system_prompt

            )

        return "Unsupported AI Provider"


engine = AIEngine()