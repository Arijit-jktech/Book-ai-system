from fastapi import APIRouter
from app.services.llama import generate_summary_from_text

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/generate-summary")
async def generate_review_summary(review_text: str):
    summary = await generate_summary_from_text(review_text, max_tokens=150)
    return {"summary": summary}
