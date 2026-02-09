"""
Image Compression API - ضغط الصور
x402 Endpoint: $0.01/request
"""

from http.server import BaseHTTPRequestHandler
import json
import base64
import io

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-402-Payment')
        self.end_headers()

    def do_GET(self):
        """API Info"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        info = {
            "name": "Image Compression API",
            "description": "Compress images to reduce file size while maintaining quality",
            "version": "1.0.0",
            "price": "$0.01 USDC/request",
            "methods": ["POST"],
            "parameters": {
                "image": "Base64 encoded image (required)",
                "quality": "Compression quality 1-100 (default: 75)",
                "format": "Output format: jpeg, png, webp (default: jpeg)"
            },
            "example": {
                "image": "base64_encoded_image_data",
                "quality": 75,
                "format": "jpeg"
            }
        }
        self.wfile.write(json.dumps(info, indent=2).encode())

    def do_POST(self):
        """Compress Image"""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            # Get parameters
            image_b64 = data.get('image', '')
            quality = min(100, max(1, int(data.get('quality', 75))))
            output_format = data.get('format', 'jpeg').lower()
            
            if not image_b64:
                self.send_error_response(400, "Missing 'image' field (base64 encoded)")
                return
            
            # Validate format
            if output_format not in ['jpeg', 'jpg', 'png', 'webp']:
                self.send_error_response(400, "Invalid format. Use: jpeg, png, or webp")
                return
            
            if output_format == 'jpg':
                output_format = 'jpeg'
            
            try:
                # Import PIL here (available on Vercel)
                from PIL import Image
                
                # Decode image
                if ',' in image_b64:
                    image_b64 = image_b64.split(',')[1]
                
                image_data = base64.b64decode(image_b64)
                original_size = len(image_data)
                
                # Open and process image
                img = Image.open(io.BytesIO(image_data))
                
                # Convert RGBA to RGB for JPEG
                if output_format == 'jpeg' and img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                
                # Compress
                output = io.BytesIO()
                
                if output_format == 'jpeg':
                    img.save(output, format='JPEG', quality=quality, optimize=True)
                elif output_format == 'png':
                    img.save(output, format='PNG', optimize=True)
                elif output_format == 'webp':
                    img.save(output, format='WEBP', quality=quality)
                
                compressed_data = output.getvalue()
                compressed_size = len(compressed_data)
                
                # Calculate compression ratio
                compression_ratio = round((1 - compressed_size / original_size) * 100, 1)
                
                # Encode result
                compressed_b64 = base64.b64encode(compressed_data).decode('utf-8')
                
                # Success response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    "success": True,
                    "image": f"data:image/{output_format};base64,{compressed_b64}",
                    "stats": {
                        "originalSize": original_size,
                        "compressedSize": compressed_size,
                        "compressionRatio": f"{compression_ratio}%",
                        "quality": quality,
                        "format": output_format,
                        "dimensions": f"{img.width}x{img.height}"
                    }
                }
                
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                self.send_error_response(400, f"Image processing error: {str(e)}")
                
        except json.JSONDecodeError:
            self.send_error_response(400, "Invalid JSON")
        except Exception as e:
            self.send_error_response(500, f"Server error: {str(e)}")
    
    def send_error_response(self, code, message):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({
            "success": False,
            "error": message
        }).encode())
