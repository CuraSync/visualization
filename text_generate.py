import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
genai.configure(api_key=API_KEY)

def generate_explanation(input_text):
    prompt = f"""
    {input_text}

    Generate a summary about this with a uneducated patient can understand using above information that provided. Explain the terms what that is what it means like vise with better explaination. minimum word limit should be 500. maximum limit should be 600. so do not include make the response like this is a chat bot or come thing just generate it in proffesional way without including unnecceery stuffs in the response.
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        response = model.generate_content(
            contents=[
                {"role": "user", "parts": [{"text": prompt}]}
            ],
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 1000,
                "top_p": 0.95
            }
        )
        
        explanation = response.text
        return explanation
    
    except Exception as e:
        return f"Error generating explanation: {str(e)}"


def save_to_file(text, filename):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(current_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(text)
        
        return f"Explanation saved to {filepath}"
    except Exception as e:
        return f"Error saving to file: {str(e)}"
    
def clean_response(text):
    lines = text.split('\n', 2)
    if len(lines) > 1:
        text = lines[2]
    else:
        text = lines[0]
    
    return text