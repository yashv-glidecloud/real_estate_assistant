from app.services.llm_service import LLMService
from app.services.search_service import SearchService


class ChatRAGService:
    def __init__(self):
        self.llm = LLMService()
        self.search = SearchService()
        self.memory = {}

    def chat(self, query: str, session_id: str = "default") -> str:
        # 🧠 INIT MEMORY
        if session_id not in self.memory:
            self.memory[session_id] = [
                {
    "role": "system",
    "content": (
        "You are an INFORMATIONAL real estate assistant.\n"
        "You DO NOT promote, advertise, compare, or recommend properties.\n"
        "You ONLY list factual property data from the provided context.\n\n"
        "Rules:\n"
        "- Use ONLY the given property data\n"
        "- Do NOT add opinions, advice, or persuasion\n"
        "- If no properties match, clearly say so\n"
        "- Show a numbered list\n"
        "- Max 5 results\n"
        "- Mention Property ID clearly\n"
        "- This is a data lookup task, NOT marketing"
    )
}
            ]

        # 🔍 SEARCH (returns FLAT dicts — NOT metadata)
        results = self.search.search(query)

        # ❌ NO RESULTS
        if not results:
            return "❌ No matching properties found for your query."

        # ✅ LIMIT TO 5
        results = results[:5]

        # 🧱 BUILD CONTEXT (USING REAL KEYS ONLY)
        context_lines = []

        for i, r in enumerate(results):
            context_lines.append(
                f"""{i + 1}. Property ID: {r.get("id")}
City: {r.get("city")}
Location: {r.get("location")}
BHK: {r.get("bhk")}
Price: ₹{r.get("price")}
Description: {r.get("description")}
"""
            )

        context = "\n".join(context_lines)

        # 🧾 PROMPT
        prompt = f"""
User query:
{query}

Matching properties:
{context}

Respond ONLY using the above properties.
"""

        # 💬 LLM CALL
        self.memory[session_id].append({
            "role": "user",
            "content": prompt
        })

        answer = self.llm.chat(self.memory[session_id])

        self.memory[session_id].append({
            "role": "assistant",
            "content": answer
        })

        return answer
