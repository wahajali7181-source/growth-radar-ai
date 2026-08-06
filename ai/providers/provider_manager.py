from config.settings import (
    OPENAI_API_KEY,
    GOOGLE_API_KEY
)


class ProviderManager:

    def __init__(self):

        self.providers = {}

        if OPENAI_API_KEY:

            self.providers["openai"] = True

        if GOOGLE_API_KEY:

            self.providers["gemini"] = True

    def available(self):

        return list(self.providers.keys())

    def has(self, provider):

        return provider in self.providers

    def default(self):

        if self.has("gemini"):

            return "gemini"

        if self.has("openai"):

            return "openai"

        return None