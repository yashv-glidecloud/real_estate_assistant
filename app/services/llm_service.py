import requests
from typing import List, Dict

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "llama3.1:8b"


class LLMService:
    def single_prompt(self, prompt: str) -> str:
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "num_ctx": 512,
                "num_predict": 120
            }
        }

        try:
            response = requests.post(
                OLLAMA_URL,
                json=payload,
                timeout=90
            )
            response.raise_for_status()
            return response.json().get("response", "").strip()

        except requests.exceptions.Timeout:
            return "⚠️ The model is taking too long. Please try again."

        except Exception as e:
            return f"❌ LLM error: {str(e)}"

    # ✅ ADD THIS METHOD
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """
        Converts chat-style messages into a single prompt
        compatible with Ollama /api/generate
        """

        prompt_parts = []

        for m in messages:
            role = m.get("role", "user").upper()
            content = m.get("content", "")
            prompt_parts.append(f"{role}:\n{content}")

        final_prompt = "\n\n".join(prompt_parts) + "\n\nASSISTANT:\n"

        return self.single_prompt(final_prompt)