import requests
import json
from config import API_KEY, API_URL, SYSTEM_PROMPT, AI_MODEL

def analyze_with_ai(base64_image: str, field_area: float):
    """
    Отправляет изображение и площадь поля в AI-модель (DeepSeek/Qwen/Claude).
    """
    payload = {
        "model": AI_MODEL,  # <-- теперь модель задаётся из .env
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Площадь поля: {field_area} гектар(а). Проанализируй фото."},
                    {"type": "image_url", "image_url": f"data:image/jpeg;base64,{base64_image}"}
                ]
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    data = response.json()

    text_output = data["choices"][0]["message"]["content"]

    try:
        result = json.loads(text_output)
        # если модель не рассчитала сезонную потерю — пересчитываем сами
        if "season_loss" not in result:
            result["season_loss"] = round(result["losses_per_ha"] * field_area, 2)
        return result
    except Exception:
        # fallback — если модель ответила нестрого JSON
        return {
            "grain_count": 0,
            "losses_per_ha": 0,
            "season_loss": 0,
            "note": text_output
        }
