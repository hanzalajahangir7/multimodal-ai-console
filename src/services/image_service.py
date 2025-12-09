import base64
from src.utils.llm import get_aclient

async def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

class ImageService:
    @staticmethod
    async def analyze_image(image_path: str, prompt: str = "Analyze this image in detail."):
        base64_image = await encode_image(image_path)
        
        aclient = get_aclient()
        response = await aclient.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )
        return response.choices[0].message.content
