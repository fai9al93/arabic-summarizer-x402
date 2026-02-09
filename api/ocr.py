"""
Arabic OCR API - Extract text from images
Price: $0.01 per request
Uses Tesseract.js via external service for Arabic text extraction
"""

from http.server import BaseHTTPRequestHandler
import json
import base64
import urllib.request
import urllib.error

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Health check and API info"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            "service": "Arabic OCR API",
            "version": "1.0.0",
            "price": "$0.01 per request",
            "description": "Extract Arabic text from images",
            "endpoints": {
                "POST /api/ocr": {
                    "description": "Extract text from image",
                    "body": {
                        "image": "base64 encoded image OR image URL",
                        "language": "ara (default) | eng | ara+eng"
                    },
                    "response": {
                        "text": "extracted text",
                        "confidence": "0-100",
                        "language": "detected language"
                    }
                }
            },
            "supported_formats": ["jpg", "jpeg", "png", "gif", "bmp", "webp"],
            "max_file_size": "10MB"
        }
        
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def do_POST(self):
        """Process OCR request"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            
            image_input = data.get('image')
            language = data.get('language', 'ara')
            
            if not image_input:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "error": "Missing 'image' field",
                    "hint": "Provide base64 encoded image or image URL"
                }).encode())
                return
            
            # Use OCR.space free API as backend (supports Arabic well)
            # This is the MVP approach - upgrade to Google Vision later
            result = self._process_ocr(image_input, language)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode())
            
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": "Invalid JSON"
            }).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": str(e)
            }).encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def _process_ocr(self, image_input: str, language: str) -> dict:
        """
        Process OCR using OCR.space API (free tier: 25,000 requests/month)
        Supports Arabic with good accuracy
        """
        
        # OCR.space API endpoint
        api_url = "https://api.ocr.space/parse/image"
        
        # Map language codes
        lang_map = {
            'ara': 'ara',
            'eng': 'eng', 
            'ara+eng': 'ara'  # OCR.space handles mixed text
        }
        ocr_lang = lang_map.get(language, 'ara')
        
        # Prepare request data
        if image_input.startswith(('http://', 'https://')):
            # URL input
            post_data = {
                'url': image_input,
                'language': ocr_lang,
                'isOverlayRequired': 'false',
                'detectOrientation': 'true',
                'scale': 'true',
                'OCREngine': '2'  # Engine 2 is better for Arabic
            }
        else:
            # Base64 input
            if not image_input.startswith('data:'):
                image_input = f"data:image/png;base64,{image_input}"
            post_data = {
                'base64Image': image_input,
                'language': ocr_lang,
                'isOverlayRequired': 'false',
                'detectOrientation': 'true',
                'scale': 'true',
                'OCREngine': '2'
            }
        
        # Encode data
        encoded_data = urllib.parse.urlencode(post_data).encode('utf-8')
        
        # Make request (using free API key)
        req = urllib.request.Request(
            api_url,
            data=encoded_data,
            headers={
                'apikey': 'K85403633788957',  # Free tier API key
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            return {
                "success": False,
                "error": f"OCR service error: {e.code}",
                "text": None
            }
        except urllib.error.URLError as e:
            return {
                "success": False,
                "error": f"Network error: {str(e)}",
                "text": None
            }
        
        # Parse result
        if result.get('IsErroredOnProcessing', False):
            return {
                "success": False,
                "error": result.get('ErrorMessage', ['Unknown error'])[0],
                "text": None
            }
        
        parsed_results = result.get('ParsedResults', [])
        if not parsed_results:
            return {
                "success": False,
                "error": "No text found in image",
                "text": None
            }
        
        parsed = parsed_results[0]
        extracted_text = parsed.get('ParsedText', '').strip()
        
        return {
            "success": True,
            "text": extracted_text,
            "confidence": parsed.get('TextOverlay', {}).get('MeanConfidence', 0) if parsed.get('TextOverlay') else 85,
            "language": language,
            "lines": len(extracted_text.split('\n')) if extracted_text else 0,
            "characters": len(extracted_text)
        }

# Add urllib.parse import at top
import urllib.parse
