import os
import openai

class EmbeddingUtil:
    def __init__(self, model: str = "text-embedding-3-small"):
        self.model = model
        self.openai = openai
        self.openai.api_key = os.getenv("OPENAI_API_KEY")

    async def generate_embedding(self, text: str) -> list:
        response = await self.openai.Embedding.acreate(
            model=self.model,
            input=text
        )
        return response["data"][0]["embedding"]
