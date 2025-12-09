from src.utils.llm import aclient
import os

class AudioService:
    @staticmethod
    async def transcribe_audio(file_path: str):
        with open(file_path, "rb") as audio_file:
            transcript = await aclient.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )
        return transcript.text

    @staticmethod
    async def analyze_audio_content(text: str, tasks: list = None):
        if not tasks:
            tasks = ["Summary", "Sentiment Analysis", "Action Items"]
        
        prompt = f"""
        Analyze the following audio transcript.
        Transcript: "{text}"
        
        Please provide:
        1. A summary.
        2. Sentiment analysis.
        3. Key topics.
        4. Action items (if any).
        5. Speaker identification clues (if apparent).
        """
        
        response = await aclient.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert audio analyst."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
