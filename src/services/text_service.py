from src.utils.llm import aclient

class TextService:
    @staticmethod
    async def analyze_text(text: str, instruction: str):
        response = await aclient.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional text analyst and editor."},
                {"role": "user", "content": f"Instruction: {instruction}\n\nText:\n{text}"}
            ]
        )
        return response.choices[0].message.content

    @staticmethod
    async def generate_json(text: str, schema_description: str):
        response = await aclient.chat.completions.create(
            model="gpt-4o",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": "You are a data extractor. Output valid JSON."},
                {"role": "user", "content": f"Extract the following structure: {schema_description}\n\nFrom this text:\n{text}"}
            ]
        )
        return response.choices[0].message.content
