"""
URL Shortener API - Test deployment
Price: $0.01 per request
"""

from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """API info"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            "service": "URL Shortener API (Test)",
            "version": "1.0.0",
            "price": "$0.01 per request",
            "description": "Test deployment - basic template",
            "status": "deployed",
            "method": "POST /api/url-shortener",
            "example": {
                "url": "https://example.com/very-long-url"
            }
        }
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def do_POST(self):
        """Shorten URL (basic template)"""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            url = data.get('url', '')
            
            if not url:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                error = {"error": "Missing 'url' parameter"}
                self.wfile.write(json.dumps(error).encode('utf-8'))
                return
            
            # Basic template response
            short_url = f"https://short.link/{hash(url) % 100000}"
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "original_url": url,
                "short_url": short_url,
                "status": "success",
                "note": "This is a test deployment - not a real shortener"
            }
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error = {"error": str(e)}
            self.wfile.write(json.dumps(error).encode('utf-8'))
