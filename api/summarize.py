import json
import os
from anthropic import Anthropic

def handler(request):
    """Vercel serverless function handler for Arabic summarization"""
    
    # Handle CORS
    if request.get('method') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': ''
        }
    
    # GET request - return info
    if request.get('method') == 'GET':
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({
                'name': 'Arabic Summarizer',
                'description': 'تلخيص النصوص العربية باستخدام AI',
                'price': '$0.01/request',
                'method': 'POST',
                'body': {
                    'text': 'النص المراد تلخيصه'
                }
            })
        }
    
    # POST request - summarize
    try:
        # Parse request body
        body = request.get('body', '{}')
        if isinstance(body, str):
            data = json.loads(body)
        else:
            data = body
        
        text = data.get('text', '').strip()
        
        if not text:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps({'error': 'Text is required'})
            }
        
        if len(text) < 50:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps({'error': 'Text too short to summarize (minimum 50 characters)'})
            }
        
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
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({
                'summary': summary,
                'original_length': len(text),
                'summary_length': len(summary),
                'compression_ratio': f"{int((1 - len(summary)/len(text)) * 100)}%"
            }, ensure_ascii=False)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({'error': str(e)})
        }
