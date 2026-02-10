# -*- coding: utf-8 -*-
"""
Arabic Summarizer API - AI-powered Arabic text summarization
Price: $0.01 per request
"""

from http.server import BaseHTTPRequestHandler
import json
import os
from anthropic import Anthropic

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """Return API info"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            'service': 'Arabic Summarizer API',
            'version': '1.0.0',
            'price': '$0.01/request',
            'description': 'تلخيص النصوص العربية باستخدام AI',
            'endpoints': {
                'POST /api/summarize': {
                    'description': 'Summarize Arabic text',
                    'body': {
                        'text': 'النص المراد تلخيصه (minimum 50 characters)'
                    },
                    'response': {
                        'summary': 'الملخص',
                        'original_length': 'عدد الأحرف الأصلي',
                        'summary_length': 'عدد أحرف الملخص',
                        'compression_ratio': 'نسبة الضغط'
                    }
                }
            }
        }
        
        self.wfile.write(json.dumps(response, ensure_ascii=False, indent=2).encode('utf-8'))
    
    def do_POST(self):
        """Summarize Arabic text"""
        try:
            # Parse request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            text = data.get('text', '').strip()
            
            # Validate input
            if not text:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': 'Text is required'
                }).encode('utf-8'))
                return
            
            if len(text) < 50:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': 'Text too short to summarize (minimum 50 characters)'
                }).encode('utf-8'))
                return
            
            # Use Anthropic API for summarization
            api_key = os.getenv('ANTHROPIC_API_KEY')
            
            if not api_key:
                # Fallback to simple extractive summarization
                sentences = text.replace('،', '.').replace('؛', '.').split('.')
                sentences = [s.strip() for s in sentences if s.strip()]
                summary = '. '.join(sentences[:3]) + '.'
            else:
                client = Anthropic(api_key=api_key)
                
                response = client.messages.create(
                    model="claude-sonnet-4-5",
                    max_tokens=500,
                    messages=[{
                        "role": "user",
                        "content": f"لخص هذا النص بشكل مختصر ومفيد (2-3 جمل):\n\n{text}"
                    }]
                )
                
                summary = response.content[0].text.strip()
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            result = {
                'summary': summary,
                'original_length': len(text),
                'summary_length': len(summary),
                'compression_ratio': f"{int((1 - len(summary)/len(text)) * 100)}%"
            }
            
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': str(e)
            }).encode('utf-8'))
