from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from deepseek_client import analyze_with_ai
from PIL import Image
import io, base64

app = FastAPI(title="AgroScope Backend (AI-ready)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "AgroScope backend is running 🚜"}
@app.post("/")
async def post_root():
    return {"error": "Используй POST /analyze для анализа изображения"}@app.post("/")
async def post_root():
    return {"error": "Используй POST /analyze для анализа изображения"}

@app.post("/analyze")
async def analyze_image(image: UploadFile = File(...), field_area: float = Form(...)):
    try:
        contents = await image.read()
        img = Image.open(io.BytesIO(contents))
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        base64_img = base64.b64encode(buffered.getvalue()).decode("utf-8")

        # передаём изображение и площадь поля в AI
        result = analyze_with_ai(base64_img, field_area)
        return result
    except Exception as e:
        return {"error": str(e)}
