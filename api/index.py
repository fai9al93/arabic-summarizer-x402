import json

def handler(request):
    """Main API endpoint - returns list of available APIs"""
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps({
            'name': 'Fofo APIs',
            'description': 'Arabic AI-powered APIs',
            'apis': [
                {
                    'name': 'Arabic Summarizer',
                    'endpoint': '/api/summarize',
                    'price': '$0.01/request',
                    'description': 'تلخيص النصوص العربية'
                },
                {
                    'name': 'Arabic OCR',
                    'endpoint': '/api/ocr',
                    'price': '$0.01/request',
                    'description': 'استخراج نص من الصور'
                }
            ],
            'documentation': 'https://arabic-summarizer-x402.vercel.app/arabic-summarizer'
        })
    }
