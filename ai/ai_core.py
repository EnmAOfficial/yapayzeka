import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_ai(prompt: str) -> str:
    """
    Kullanıcı mesajını OpenAI'e gönderir ve cevabı döndürür.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Sen profesyonel bir Discord destek yapay zekasısın."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ Yapay zekâ hatası oluştu: {str(e)}"
