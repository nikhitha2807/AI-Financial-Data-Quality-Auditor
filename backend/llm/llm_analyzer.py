import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            print("Warning: GROQ_API_KEY not found in environment.")
        self.client = Groq(api_key=self.api_key) if self.api_key else None

    async def analyze_summary(self, profile: dict, issues: list, score: dict):
        if not self.client:
            return "Groq API Key not configured. AI Analysis unavailable."

        prompt = f"""
        You are a data quality expert. Analyze the following dataset summary and provide a professional assessment.
        
        ### Dataset Profile:
        - Row Count: {profile['row_count']}
        - Column Count: {profile['column_count']}
        - Overall Quality Score: {score['overall_score']}/100
        
        ### Detected Issues:
        {issues}
        
        Provide:
        1. A high-level data quality explanation.
        2. Summary of key detected issues.
        3. Clear suggested cleaning steps.
        4. Long-term data improvement recommendations.
        
        Format the output in clear Markdown.
        """
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a professional Data Quality Analyst."},
                    {"role": "user", "content": prompt}
                ],
                model="llama3-8b-8192", # Defaulting to Llama 3 on Groq
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error during AI analysis: {str(e)}"
