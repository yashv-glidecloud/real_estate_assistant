from typing import List, Dict

class ChatService:
    def generate_response(
        self,
        user_query: str,
        parsed_query: Dict,
        results: List[Dict]
    ) -> Dict:
        if not results:
            return {
                "answer": (
                    "I couldn't find any properties matching your requirements. "
                    "Would you like to relax the budget or try a nearby area?"
                ),
                "results": []
            }

        city = parsed_query.get("city")
        bhk = parsed_query.get("bhk")
        price_max = parsed_query.get("price_max")
        balcony = parsed_query.get("balcony")

        intro_parts = []

        if bhk:
            intro_parts.append(f"{bhk}BHK")
        intro_parts.append("apartments")

        if city:
            intro_parts.append(f"in {city}")

        if price_max:
            intro_parts.append(f"under ₹{price_max // 100000} lakhs")

        if balcony:
            intro_parts.append("with a balcony")

        intro_sentence = " ".join(intro_parts)

        response_text = (
            f"I found {len(results)} {intro_sentence}. "
            "Here are some good options:\n"
        )

        bullet_points = []
        for r in results[:3]:
            meta = r["metadata"]
            price_lakhs = meta["price"] // 100000

            bullet_points.append(
                f"- {meta['bhk']}BHK in {meta['area']} priced at ₹{price_lakhs} lakhs "
                f"({meta['price_category']}, {meta['bathrooms']} bathrooms)"
            )

        response_text += "\n".join(bullet_points)
        response_text += "\n\nWould you like properties closer to offices, metro stations, or within a lower budget?"

        return {
            "answer": response_text,
            "results": results
        }
