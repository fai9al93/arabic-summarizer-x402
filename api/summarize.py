from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os

app = FastAPI()

class SummarizeRequest(BaseModel):
    text: str
    max_length: Optional[int] = 200
    language: Optional[str] = "ar"

class SummarizeResponse(BaseModel):
    summary: str
    original_length: int
    summary_length: int
    success: bool

@app.post("/api/summarize")
async def summarize(request: SummarizeRequest) -> SummarizeResponse:
    """تلخيص النص العربي"""
    try:
        text = request.text.strip()
        
        if not text:
            raise HTTPException(status_code=400, detail="Text is required")
        
        if len(text) < 50:
            raise HTTPException(status_code=400, detail="Text too short to summarize")
        
        # Simple extractive summarization
        sentences = text.replace('،', '.').replace('؛', '.').split('.')
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Take first few sentences up to max_length
        summary_parts = []
        current_length = 0
        
        for sentence in sentences:
            if current_length + len(sentence) <= request.max_length:
                summary_parts.append(sentence)
                current_length += len(sentence)
            else:
                break
        
        if not summary_parts and sentences:
            # Take first sentence truncated
            summary_parts = [sentences[0][:request.max_length]]
        
        summary = '. '.join(summary_parts)
        if summary and not summary.endswith('.'):
            summary += '.'
        
        return SummarizeResponse(
            summary=summary,
            original_length=len(text),
            summary_length=len(summary),
            success=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/summarize")
async def summarize_info():
    return {
        "name": "Arabic Summarizer",
        "description": "تلخيص النصوص العربية",
        "price": "$0.01/request",
        "method": "POST",
        "body": {
            "text": "النص المراد تلخيصه",
            "max_length": "الحد الأقصى (اختياري)",
            "language": "اللغة (اختياري)"
        }
    }
