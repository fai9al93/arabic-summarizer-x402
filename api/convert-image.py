from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import Response
from typing import Optional
from io import BytesIO
import base64

app = FastAPI()

# Note: PIL needs to be installed
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

SUPPORTED_FORMATS = ["png", "jpg", "jpeg", "webp", "gif", "bmp"]

@app.post("/api/convert-image")
async def convert_image(
    file: UploadFile = File(...),
    format: str = "png",
    quality: int = 85
):
    """تحويل صيغة الصورة"""
    try:
        if not PIL_AVAILABLE:
            raise HTTPException(status_code=500, detail="PIL not available")
        
        format = format.lower()
        if format not in SUPPORTED_FORMATS:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported format. Use: {', '.join(SUPPORTED_FORMATS)}"
            )
        
        # Read image
        contents = await file.read()
        img = Image.open(BytesIO(contents))
        
        # Convert RGBA to RGB for JPEG
        if format in ["jpg", "jpeg"] and img.mode == "RGBA":
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        
        # Save to buffer
        buffer = BytesIO()
        save_format = "JPEG" if format in ["jpg", "jpeg"] else format.upper()
        
        if format in ["jpg", "jpeg", "webp"]:
            img.save(buffer, format=save_format, quality=quality)
        else:
            img.save(buffer, format=save_format)
        
        buffer.seek(0)
        
        # Return as base64 or binary
        content_types = {
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "webp": "image/webp",
            "gif": "image/gif",
            "bmp": "image/bmp"
        }
        
        return Response(
            content=buffer.getvalue(),
            media_type=content_types.get(format, "application/octet-stream"),
            headers={
                "Content-Disposition": f"attachment; filename=converted.{format}"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/convert-image")
async def convert_info():
    return {
        "name": "Image Format Converter",
        "description": "تحويل صيغ الصور",
        "price": "$0.01/request",
        "method": "POST",
        "content_type": "multipart/form-data",
        "params": {
            "file": "الصورة (required)",
            "format": f"الصيغة المطلوبة: {', '.join(SUPPORTED_FORMATS)}",
            "quality": "الجودة 1-100 (للـ jpg/webp)"
        }
    }
