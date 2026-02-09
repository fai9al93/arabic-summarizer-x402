from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Fofo APIs", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

LANDING_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fofo APIs - Simple APIs for Complex Problems</title>
    <meta name="description" content="AI-powered APIs with pay-per-use pricing. Arabic summarizer, data validator, image converter. No subscriptions, no API keys.">
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --accent: #c8ff00;
            --accent-dim: rgba(200, 255, 0, 0.1);
            --white: #ffffff;
            --gray: #888888;
            --dark: #0a0a0a;
            --card: #111;
            --success: #00ff88;
            --error: #ff4444;
        }
        
        body {
            font-family: 'Space Grotesk', sans-serif;
            background: var(--dark);
            color: var(--white);
            overflow-x: hidden;
        }
        
        ::selection { background: var(--accent); color: var(--dark); }
        
        /* Navigation */
        nav {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            padding: 20px 48px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 100;
            background: rgba(10,10,10,0.9);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        
        .logo { font-size: 1.2rem; font-weight: 600; letter-spacing: -0.5px; }
        
        .status-badge {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 6px 14px;
            background: rgba(0, 255, 136, 0.1);
            border: 1px solid rgba(0, 255, 136, 0.3);
            border-radius: 50px;
            font-size: 0.75rem;
            color: var(--success);
        }
        
        .status-dot {
            width: 6px;
            height: 6px;
            background: var(--success);
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .nav-links {
            display: flex;
            gap: 32px;
            list-style: none;
        }
        
        .nav-links a {
            color: var(--white);
            text-decoration: none;
            font-size: 0.85rem;
            opacity: 0.7;
            transition: opacity 0.3s;
        }
        
        .nav-links a:hover { opacity: 1; }
        
        .nav-cta {
            padding: 10px 20px;
            border: 1px solid rgba(255,255,255,0.3);
            border-radius: 50px;
            font-size: 0.85rem;
            color: var(--white);
            text-decoration: none;
            transition: all 0.3s;
        }
        
        .nav-cta:hover { background: var(--white); color: var(--dark); }
        
        /* Hero */
        .hero {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 120px 48px;
            position: relative;
        }
        
        .hero-label {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            opacity: 0.5;
            margin-bottom: 24px;
        }
        
        .hero h1 {
            font-size: clamp(3.5rem, 12vw, 10rem);
            font-weight: 500;
            line-height: 0.9;
            letter-spacing: -0.04em;
            margin-bottom: 48px;
        }
        
        .hero h1 span { display: block; }
        .hero h1 .outline {
            -webkit-text-stroke: 1px var(--white);
            -webkit-text-fill-color: transparent;
        }
        
        .hero-desc {
            max-width: 400px;
            font-size: 1rem;
            line-height: 1.7;
            opacity: 0.6;
            margin-left: auto;
            margin-right: 10%;
        }
        
        .scroll-indicator {
            position: absolute;
            bottom: 48px;
            left: 48px;
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 0.75rem;
            opacity: 0.5;
        }
        
        .scroll-line { width: 48px; height: 1px; background: var(--white); }
        
        /* Sections */
        section { padding: 100px 48px; }
        
        .section-label {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 60px;
        }
        
        .section-label::before {
            content: '';
            width: 8px;
            height: 8px;
            background: var(--accent);
            border-radius: 50%;
        }
        
        /* APIs */
        .apis-intro {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 80px;
            margin-bottom: 80px;
        }
        
        .apis-intro h2 {
            font-size: clamp(2rem, 4vw, 3rem);
            font-weight: 500;
            line-height: 1.2;
        }
        
        .apis-intro p {
            font-size: 1rem;
            line-height: 1.8;
            opacity: 0.6;
        }
        
        .api-cards { display: grid; gap: 2px; background: rgba(255,255,255,0.1); }
        
        .api-card {
            background: var(--dark);
            padding: 40px;
            transition: background 0.3s;
        }
        
        .api-card:hover { background: var(--card); }
        
        .api-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 20px;
        }
        
        .api-number { font-size: 0.85rem; opacity: 0.4; }
        
        .api-title { font-size: 1.4rem; font-weight: 500; margin: 8px 0; }
        
        .api-desc { font-size: 0.9rem; opacity: 0.5; line-height: 1.6; margin-bottom: 16px; }
        
        .api-endpoint {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            color: var(--accent);
            background: var(--accent-dim);
            padding: 8px 14px;
            border-radius: 4px;
            display: inline-block;
        }
        
        .api-price {
            font-size: 1.4rem;
            font-weight: 600;
            color: var(--accent);
        }
        
        .api-price span { font-size: 0.8rem; font-weight: 400; opacity: 0.6; color: var(--white); }
        
        /* Code Examples */
        .code-section { margin-top: 24px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 24px; }
        
        .code-tabs { display: flex; gap: 8px; margin-bottom: 12px; flex-wrap: wrap; }
        
        .tab {
            padding: 8px 16px;
            background: transparent;
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 4px;
            color: var(--white);
            font-size: 0.75rem;
            cursor: pointer;
            transition: all 0.2s;
            font-family: inherit;
        }
        
        .tab:hover { border-color: var(--accent); }
        .tab.active { background: var(--accent); color: var(--dark); border-color: var(--accent); }
        
        .code-block {
            background: #1a1a1a;
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 8px;
            padding: 16px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            line-height: 1.6;
            overflow-x: auto;
            color: #e0e0e0;
            white-space: pre-wrap;
        }
        
        .code-block.hidden { display: none; }
        
        .response-box {
            margin-top: 12px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }
        
        .response-item {
            padding: 14px;
            border-radius: 8px;
            font-size: 0.75rem;
        }
        
        .response-success {
            background: rgba(0, 255, 136, 0.05);
            border: 1px solid rgba(0, 255, 136, 0.2);
        }
        
        .response-error {
            background: rgba(255, 68, 68, 0.05);
            border: 1px solid rgba(255, 68, 68, 0.2);
        }
        
        .response-label {
            font-size: 0.65rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
            display: block;
        }
        
        .response-success .response-label { color: var(--success); }
        .response-error .response-label { color: var(--error); }
        
        .response-item pre {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem;
            color: #a0a0a0;
            margin: 0;
            white-space: pre-wrap;
        }
        
        /* Try It Live */
        .try-section {
            margin-top: 20px;
            padding: 20px;
            background: rgba(200, 255, 0, 0.03);
            border: 1px solid rgba(200, 255, 0, 0.15);
            border-radius: 12px;
        }
        
        .try-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 16px;
            font-size: 0.85rem;
            font-weight: 500;
        }
        
        .try-header span { color: var(--accent); }
        
        .try-input {
            width: 100%;
            padding: 14px;
            background: #1a1a1a;
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 8px;
            color: var(--white);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            resize: vertical;
            min-height: 80px;
            margin-bottom: 12px;
        }
        
        .try-input:focus { outline: none; border-color: var(--accent); }
        
        .try-btn {
            padding: 12px 24px;
            background: var(--accent);
            color: var(--dark);
            border: none;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.85rem;
            cursor: pointer;
            transition: transform 0.2s;
            font-family: inherit;
        }
        
        .try-btn:hover { transform: scale(1.02); }
        .try-btn:disabled { opacity: 0.5; cursor: not-allowed; }
        
        .try-result {
            margin-top: 16px;
            padding: 16px;
            background: #1a1a1a;
            border-radius: 8px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            display: none;
        }
        
        .try-result.show { display: block; }
        .try-result.success { border: 1px solid rgba(0, 255, 136, 0.3); }
        .try-result.error { border: 1px solid rgba(255, 68, 68, 0.3); }
        
        /* Rate Limits */
        .limits-section {
            background: var(--card);
            border-radius: 16px;
            padding: 60px;
            margin: 60px 0;
        }
        
        .limits-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 32px;
            margin-top: 40px;
        }
        
        .limit-item { text-align: center; }
        
        .limit-value {
            font-size: 2.5rem;
            font-weight: 600;
            color: var(--accent);
            margin-bottom: 8px;
        }
        
        .limit-label { font-size: 0.85rem; opacity: 0.6; }
        
        /* Payment */
        .payment-section {
            background: linear-gradient(135deg, #111 0%, #0a0a0a 100%);
            border: 1px solid rgba(200, 255, 0, 0.2);
            border-radius: 16px;
            padding: 60px;
            margin: 60px 0;
        }
        
        .payment-header {
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 24px;
        }
        
        .payment-badge {
            background: var(--accent);
            color: var(--dark);
            padding: 8px 16px;
            border-radius: 50px;
            font-size: 0.85rem;
            font-weight: 600;
        }
        
        .payment-title { font-size: 1.5rem; font-weight: 500; }
        
        .payment-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 32px;
            margin-top: 40px;
        }
        
        .payment-feature { text-align: center; padding: 24px; }
        .payment-icon { font-size: 2rem; margin-bottom: 16px; }
        .payment-feature h4 { font-size: 1rem; margin-bottom: 8px; }
        .payment-feature p { font-size: 0.85rem; opacity: 0.6; line-height: 1.6; }
        
        /* FAQ */
        .faq-section { margin: 60px 0; }
        
        .faq-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 24px;
            margin-top: 40px;
        }
        
        .faq-item {
            background: var(--card);
            border-radius: 12px;
            padding: 28px;
        }
        
        .faq-q {
            font-size: 1rem;
            font-weight: 500;
            margin-bottom: 12px;
            color: var(--accent);
        }
        
        .faq-a { font-size: 0.9rem; opacity: 0.7; line-height: 1.7; }
        
        /* Changelog */
        .changelog-section {
            margin: 60px 0;
            padding: 40px;
            background: var(--card);
            border-radius: 16px;
        }
        
        .changelog-item {
            display: flex;
            gap: 24px;
            padding: 20px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        
        .changelog-item:last-child { border-bottom: none; }
        
        .changelog-date {
            font-size: 0.8rem;
            opacity: 0.5;
            min-width: 100px;
        }
        
        .changelog-content h4 {
            font-size: 0.95rem;
            margin-bottom: 8px;
        }
        
        .changelog-content p { font-size: 0.85rem; opacity: 0.6; }
        
        .changelog-tag {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.7rem;
            font-weight: 500;
            margin-right: 8px;
        }
        
        .tag-new { background: rgba(0, 255, 136, 0.15); color: var(--success); }
        .tag-improved { background: rgba(200, 255, 0, 0.15); color: var(--accent); }
        
        /* CTA */
        .cta { padding: 120px 48px; text-align: center; }
        
        .cta h2 {
            font-size: clamp(2rem, 6vw, 4rem);
            font-weight: 500;
            margin-bottom: 40px;
        }
        
        .cta-btn {
            display: inline-flex;
            align-items: center;
            gap: 12px;
            padding: 18px 36px;
            background: var(--accent);
            color: var(--dark);
            text-decoration: none;
            font-weight: 600;
            font-size: 1rem;
            border-radius: 50px;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .cta-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 20px 60px rgba(200, 255, 0, 0.3);
        }
        
        /* Footer */
        footer {
            padding: 48px;
            border-top: 1px solid rgba(255,255,255,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        footer p { font-size: 0.85rem; opacity: 0.5; }
        footer a { color: var(--accent); text-decoration: none; }
        
        .footer-links { display: flex; gap: 32px; }
        
        .footer-links a {
            font-size: 0.85rem;
            color: var(--white);
            opacity: 0.5;
            text-decoration: none;
            transition: opacity 0.3s;
        }
        
        .footer-links a:hover { opacity: 1; }
        
        /* Responsive */
        @media (max-width: 900px) {
            nav { padding: 16px 24px; }
            .nav-links { display: none; }
            .status-badge { display: none; }
            section { padding: 60px 24px; }
            .hero { padding: 100px 24px; }
            .hero h1 { font-size: 2.5rem; }
            .hero-desc { margin: 32px 0 0 0; }
            .apis-intro { grid-template-columns: 1fr; gap: 32px; }
            .api-header { flex-direction: column; gap: 16px; }
            .response-box { grid-template-columns: 1fr; }
            .limits-grid { grid-template-columns: repeat(2, 1fr); }
            .payment-grid { grid-template-columns: 1fr; }
            .faq-grid { grid-template-columns: 1fr; }
            footer { flex-direction: column; gap: 24px; text-align: center; }
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .hero h1, .hero-desc, .section-label, .api-card {
            animation: fadeIn 0.8s ease-out forwards;
        }
    </style>
</head>
<body>
    <nav>
        <div class="logo">Fofo°</div>
        <div class="status-badge">
            <span class="status-dot"></span>
            99.9% Uptime
        </div>
        <ul class="nav-links">
            <li><a href="#apis">APIs</a></li>
            <li><a href="#limits">Limits</a></li>
            <li><a href="#payment">Payment</a></li>
            <li><a href="#faq">FAQ</a></li>
            <li><a href="/hawas" style="color: #D4A574;">☕ Hawas</a></li>
            <li><a href="https://x.com/Fai9al_fofo">Twitter</a></li>
        </ul>
        <a href="#try-summarize" class="nav-cta">try it live</a>
    </nav>
    
    <section class="hero">
        <p class="hero-label">AI-Powered API Services</p>
        <h1>
            <span>build</span>
            <span class="outline">faster.</span>
        </h1>
        <p class="hero-desc">
            Simple, powerful APIs that help developers ship products faster. 
            Pay only for what you use. No subscriptions, no API keys.
        </p>
        <div class="scroll-indicator">
            <div class="scroll-line"></div>
            scroll
        </div>
    </section>
    
    <section id="apis">
        <p class="section-label">our services</p>
        
        <div class="apis-intro">
            <h2>Simple APIs for complex problems.</h2>
            <p>Each API is designed to solve a specific problem efficiently. Clean documentation, predictable pricing, and reliable uptime.</p>
        </div>
        
        <div class="api-cards">
            <!-- API 1: Summarize -->
            <div class="api-card">
                <div class="api-header">
                    <div>
                        <span class="api-number">01.</span>
                        <h3 class="api-title">Arabic Text Summarizer</h3>
                        <p class="api-desc">Summarize Arabic content with AI. Perfect for news apps, research tools, and content platforms.</p>
                        <code class="api-endpoint">POST /api/summarize</code>
                    </div>
                    <div class="api-price">$0.01<span>/req</span></div>
                </div>
                
                <div class="code-section">
                    <div class="code-tabs">
                        <button class="tab active" onclick="showTab(this, 'curl1')">cURL</button>
                        <button class="tab" onclick="showTab(this, 'python1')">Python</button>
                        <button class="tab" onclick="showTab(this, 'js1')">JavaScript</button>
                    </div>
                    <pre class="code-block" id="curl1">curl -X POST https://fofo-apis-vercel.vercel.app/api/summarize \\
  -H "Content-Type: application/json" \\
  -d '{"text": "النص العربي هنا...", "max_length": 100}'</pre>
                    <pre class="code-block hidden" id="python1">import requests

response = requests.post(
    "https://fofo-apis-vercel.vercel.app/api/summarize",
    json={"text": "النص العربي هنا...", "max_length": 100}
)
print(response.json())</pre>
                    <pre class="code-block hidden" id="js1">fetch("https://fofo-apis-vercel.vercel.app/api/summarize", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ text: "النص العربي هنا...", max_length: 100 })
}).then(r => r.json()).then(console.log)</pre>
                    
                    <div class="response-box">
                        <div class="response-item response-success">
                            <span class="response-label">✓ Success (200)</span>
                            <pre>{"summary": "ملخص النص...", "original_length": 500, "summary_length": 95}</pre>
                        </div>
                        <div class="response-item response-error">
                            <span class="response-label">✗ Error (400)</span>
                            <pre>{"error": "Text is required", "code": "MISSING_TEXT"}</pre>
                        </div>
                    </div>
                </div>
                
                <div class="try-section" id="try-summarize">
                    <div class="try-header">
                        <span>⚡</span> Try it live
                    </div>
                    <textarea class="try-input" id="input1" placeholder="أدخل النص العربي هنا للتلخيص...">الذكاء الاصطناعي هو فرع من علوم الحاسوب يهدف إلى إنشاء أنظمة قادرة على أداء مهام تتطلب عادةً ذكاءً بشريًا. يشمل ذلك التعلم والاستدلال وحل المشكلات والإدراك وفهم اللغة الطبيعية.</textarea>
                    <button class="try-btn" onclick="tryAPI('summarize', 'input1', 'result1')">Run Request →</button>
                    <div class="try-result" id="result1"></div>
                </div>
            </div>
            
            <!-- API 2: Validate -->
            <div class="api-card">
                <div class="api-header">
                    <div>
                        <span class="api-number">02.</span>
                        <h3 class="api-title">Data Validator</h3>
                        <p class="api-desc">Validate emails, phones, URLs and custom data with smart auto-detection and flexible rules.</p>
                        <code class="api-endpoint">POST /api/validate</code>
                    </div>
                    <div class="api-price">$0.02<span>/req</span></div>
                </div>
                
                <div class="code-section">
                    <div class="code-tabs">
                        <button class="tab active" onclick="showTab(this, 'curl2')">cURL</button>
                        <button class="tab" onclick="showTab(this, 'python2')">Python</button>
                        <button class="tab" onclick="showTab(this, 'js2')">JavaScript</button>
                    </div>
                    <pre class="code-block" id="curl2">curl -X POST https://fofo-apis-vercel.vercel.app/api/validate \\
  -H "Content-Type: application/json" \\
  -d '{"data": "test@example.com", "type": "email"}'</pre>
                    <pre class="code-block hidden" id="python2">import requests

response = requests.post(
    "https://fofo-apis-vercel.vercel.app/api/validate",
    json={"data": "test@example.com", "type": "email"}
)
print(response.json())</pre>
                    <pre class="code-block hidden" id="js2">fetch("https://fofo-apis-vercel.vercel.app/api/validate", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ data: "test@example.com", type: "email" })
}).then(r => r.json()).then(console.log)</pre>
                    
                    <div class="response-box">
                        <div class="response-item response-success">
                            <span class="response-label">✓ Success (200)</span>
                            <pre>{"valid": true, "type": "email", "details": {"domain": "example.com"}}</pre>
                        </div>
                        <div class="response-item response-error">
                            <span class="response-label">✗ Error (400)</span>
                            <pre>{"valid": false, "error": "Invalid format"}</pre>
                        </div>
                    </div>
                </div>
                
                <div class="try-section">
                    <div class="try-header">
                        <span>⚡</span> Try it live
                    </div>
                    <textarea class="try-input" id="input2" placeholder="Enter email, phone, or URL to validate...">test@example.com</textarea>
                    <button class="try-btn" onclick="tryAPI('validate', 'input2', 'result2')">Run Request →</button>
                    <div class="try-result" id="result2"></div>
                </div>
            </div>
            
            <!-- API 3: Arabic OCR -->
            <div class="api-card">
                <div class="api-header">
                    <div>
                        <span class="api-number">03.</span>
                        <h3 class="api-title">Arabic OCR</h3>
                        <p class="api-desc">Extract Arabic text from images. Perfect for document scanning, receipt processing, and form digitization.</p>
                        <code class="api-endpoint">POST /api/ocr</code>
                    </div>
                    <div class="api-price">$0.01<span>/req</span></div>
                </div>
                
                <div class="code-section">
                    <div class="code-tabs">
                        <button class="tab active" onclick="showTab(this, 'curl_ocr')">cURL</button>
                        <button class="tab" onclick="showTab(this, 'python_ocr')">Python</button>
                        <button class="tab" onclick="showTab(this, 'js_ocr')">JavaScript</button>
                    </div>
                    <pre class="code-block" id="curl_ocr">curl -X POST https://fofo-apis-vercel.vercel.app/api/ocr \\
  -H "Content-Type: application/json" \\
  -d '{"image": "https://example.com/arabic-doc.jpg", "language": "ara"}'</pre>
                    <pre class="code-block hidden" id="python_ocr">import requests

response = requests.post(
    "https://fofo-apis-vercel.vercel.app/api/ocr",
    json={"image": "https://example.com/arabic-doc.jpg", "language": "ara"}
)
print(response.json())</pre>
                    <pre class="code-block hidden" id="js_ocr">fetch("https://fofo-apis-vercel.vercel.app/api/ocr", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ image: "https://example.com/arabic-doc.jpg", language: "ara" })
}).then(r => r.json()).then(console.log)</pre>
                    
                    <div class="response-box">
                        <div class="response-item response-success">
                            <span class="response-label">✓ Success (200)</span>
                            <pre>{"success": true, "text": "النص المستخرج...", "confidence": 92}</pre>
                        </div>
                        <div class="response-item response-error">
                            <span class="response-label">✗ Error (400)</span>
                            <pre>{"success": false, "error": "No text found in image"}</pre>
                        </div>
                    </div>
                </div>
                
                <div class="try-section">
                    <div class="try-header">
                        <span>⚡</span> Try it live
                    </div>
                    <textarea class="try-input" id="input_ocr" placeholder="Enter image URL...">https://upload.wikimedia.org/wikipedia/commons/a/a5/Arabic_Text.png</textarea>
                    <button class="try-btn" onclick="tryOCR()">Run Request →</button>
                    <div class="try-result" id="result_ocr"></div>
                </div>
            </div>
            
            <!-- API 4: Convert Image -->
            <div class="api-card">
                <div class="api-header">
                    <div>
                        <span class="api-number">04.</span>
                        <h3 class="api-title">Image Converter</h3>
                        <p class="api-desc">Convert images between formats. Supports PNG, JPG, WebP, GIF, BMP with quality control.</p>
                        <code class="api-endpoint">POST /api/convert-image</code>
                    </div>
                    <div class="api-price">$0.01<span>/req</span></div>
                </div>
                
                <div class="code-section">
                    <div class="code-tabs">
                        <button class="tab active" onclick="showTab(this, 'curl3')">cURL</button>
                        <button class="tab" onclick="showTab(this, 'python3')">Python</button>
                        <button class="tab" onclick="showTab(this, 'js3')">JavaScript</button>
                    </div>
                    <pre class="code-block" id="curl3">curl -X POST https://fofo-apis-vercel.vercel.app/api/convert-image \\
  -H "Content-Type: application/json" \\
  -d '{"image": "base64_or_url", "format": "webp", "quality": 85}'</pre>
                    <pre class="code-block hidden" id="python3">import requests

response = requests.post(
    "https://fofo-apis-vercel.vercel.app/api/convert-image",
    json={"image": "https://example.com/image.png", "format": "webp", "quality": 85}
)
print(response.json())</pre>
                    <pre class="code-block hidden" id="js3">fetch("https://fofo-apis-vercel.vercel.app/api/convert-image", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ image: "https://example.com/image.png", format: "webp", quality: 85 })
}).then(r => r.json()).then(console.log)</pre>
                    
                    <div class="response-box">
                        <div class="response-item response-success">
                            <span class="response-label">✓ Success (200)</span>
                            <pre>{"image": "base64...", "format": "webp", "size": 12480}</pre>
                        </div>
                        <div class="response-item response-error">
                            <span class="response-label">✗ Error (400)</span>
                            <pre>{"error": "Invalid image", "code": "INVALID_INPUT"}</pre>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    
    <!-- Rate Limits -->
    <section id="limits">
        <p class="section-label">rate limits</p>
        <div class="limits-section">
            <h2 style="font-size: 2rem; margin-bottom: 16px;">Fair Usage Policy</h2>
            <p style="opacity: 0.6; max-width: 600px;">We believe in generous limits. Most developers never hit them.</p>
            
            <div class="limits-grid">
                <div class="limit-item">
                    <div class="limit-value">100</div>
                    <div class="limit-label">Requests / minute</div>
                </div>
                <div class="limit-item">
                    <div class="limit-value">10K</div>
                    <div class="limit-label">Requests / day</div>
                </div>
                <div class="limit-item">
                    <div class="limit-value">5MB</div>
                    <div class="limit-label">Max payload size</div>
                </div>
                <div class="limit-item">
                    <div class="limit-value">30s</div>
                    <div class="limit-label">Request timeout</div>
                </div>
            </div>
        </div>
    </section>
    
    <!-- Payment -->
    <section id="payment">
        <div class="payment-section">
            <div class="payment-header">
                <span class="payment-badge">x402 Protocol</span>
                <h3 class="payment-title">Pay with Crypto. No API Keys.</h3>
            </div>
            <p style="opacity: 0.6; max-width: 600px; line-height: 1.7;">
                Our APIs use the x402 payment protocol. Pay directly with USDC on Base network. 
                No registration, no API keys, no monthly subscriptions.
            </p>
            <div class="payment-grid">
                <div class="payment-feature">
                    <div class="payment-icon">⚡</div>
                    <h4>Instant Access</h4>
                    <p>No signup required. Start making API calls immediately after payment.</p>
                </div>
                <div class="payment-feature">
                    <div class="payment-icon">🔐</div>
                    <h4>Secure & Private</h4>
                    <p>On-chain payments. No credit cards, no personal data collection.</p>
                </div>
                <div class="payment-feature">
                    <div class="payment-icon">💰</div>
                    <h4>Pay What You Use</h4>
                    <p>Micro-payments per request. No minimums, no commitments.</p>
                </div>
            </div>
        </div>
    </section>
    
    <!-- FAQ -->
    <section id="faq">
        <p class="section-label">frequently asked questions</p>
        <div class="faq-grid">
            <div class="faq-item">
                <h4 class="faq-q">How do I pay for API requests?</h4>
                <p class="faq-a">We use the x402 protocol. Your wallet pays automatically per request using USDC on Base network. No API keys needed.</p>
            </div>
            <div class="faq-item">
                <h4 class="faq-q">What if I exceed rate limits?</h4>
                <p class="faq-a">You'll receive a 429 status code. Wait a minute and retry. Contact us for higher limits if needed.</p>
            </div>
            <div class="faq-item">
                <h4 class="faq-q">Is there a free tier?</h4>
                <p class="faq-a">The Try It Live feature is free for testing. Production use requires payment via x402.</p>
            </div>
            <div class="faq-item">
                <h4 class="faq-q">What's the uptime guarantee?</h4>
                <p class="faq-a">We target 99.9% uptime. APIs are deployed on Vercel's edge network for maximum reliability.</p>
            </div>
            <div class="faq-item">
                <h4 class="faq-q">Can I get a refund?</h4>
                <p class="faq-a">Failed requests (5xx errors) are not charged. You only pay for successful responses.</p>
            </div>
            <div class="faq-item">
                <h4 class="faq-q">Need help or custom solutions?</h4>
                <p class="faq-a">DM us on Twitter <a href="https://x.com/Fai9al_fofo" style="color: var(--accent);">@Fai9al_fofo</a> for support or enterprise inquiries.</p>
            </div>
        </div>
    </section>
    
    <!-- Changelog -->
    <section id="changelog">
        <p class="section-label">changelog</p>
        <div class="changelog-section">
            <div class="changelog-item">
                <div class="changelog-date">Feb 9, 2026</div>
                <div class="changelog-content">
                    <h4><span class="changelog-tag tag-new">NEW</span> Arabic OCR API</h4>
                    <p>Extract Arabic text from images. Supports scanned documents, receipts, and handwritten text.</p>
                </div>
            </div>
            <div class="changelog-item">
                <div class="changelog-date">Feb 8, 2026</div>
                <div class="changelog-content">
                    <h4><span class="changelog-tag tag-new">NEW</span> Website Redesign</h4>
                    <p>Complete redesign with Try It Live feature, code examples, FAQ, and better documentation.</p>
                </div>
            </div>
            <div class="changelog-item">
                <div class="changelog-date">Feb 5, 2026</div>
                <div class="changelog-content">
                    <h4><span class="changelog-tag tag-new">NEW</span> Image Converter API</h4>
                    <p>Convert images between PNG, JPG, WebP, GIF, and BMP with quality control.</p>
                </div>
            </div>
            <div class="changelog-item">
                <div class="changelog-date">Feb 3, 2026</div>
                <div class="changelog-content">
                    <h4><span class="changelog-tag tag-improved">IMPROVED</span> Validation API</h4>
                    <p>Added phone number validation with country detection and URL validation.</p>
                </div>
            </div>
            <div class="changelog-item">
                <div class="changelog-date">Feb 1, 2026</div>
                <div class="changelog-content">
                    <h4><span class="changelog-tag tag-new">NEW</span> Initial Launch</h4>
                    <p>Launched Arabic Text Summarizer and Data Validator APIs with x402 payments.</p>
                </div>
            </div>
        </div>
    </section>
    
    <!-- Hawas App -->
    <section id="hawas" style="padding: 80px 48px; background: var(--card); border-top: 1px solid rgba(255,255,255,0.1);">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 60px; align-items: center; max-width: 1200px; margin: 0 auto;">
            <div>
                <p style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; color: var(--accent); margin-bottom: 16px;">☕ Our App</p>
                <h2 style="font-size: clamp(2rem, 4vw, 3rem); font-weight: 500; margin-bottom: 24px; line-height: 1.2;">Hawas<br><span style="opacity: 0.5;">Coffee Discovery Reimagined</span></h2>
                <p style="font-size: 1rem; line-height: 1.8; opacity: 0.7; margin-bottom: 32px;">
                    Scan any coffee bag with AI. Build your collection. Complete epic journeys. 
                    The ultimate app for specialty coffee lovers.
                </p>
                <div style="display: flex; gap: 16px; flex-wrap: wrap;">
                    <a href="/hawas" style="display: inline-flex; align-items: center; gap: 8px; padding: 14px 28px; background: var(--accent); color: var(--dark); text-decoration: none; font-weight: 600; border-radius: 50px; transition: transform 0.3s;">
                        Learn More →
                    </a>
                    <a href="https://testflight.apple.com/join/SDte6VFJ" style="display: inline-flex; align-items: center; gap: 8px; padding: 14px 28px; border: 1px solid rgba(200, 255, 0, 0.5); color: var(--accent); text-decoration: none; font-weight: 500; border-radius: 50px;">
                        TestFlight ↗
                    </a>
                </div>
            </div>
            <div style="text-align: center;">
                <div style="background: linear-gradient(135deg, #c8ff00 0%, #7a9900 100%); width: 200px; height: 200px; border-radius: 40px; margin: 0 auto; display: flex; align-items: center; justify-content: center; box-shadow: 0 20px 60px rgba(200, 255, 0, 0.2); padding: 30px;">
                    <img src="/hawas/images/hawas-logo.svg" alt="Hawas Logo" style="width: 100%; height: 100%; filter: brightness(0);">
                </div>
            </div>
        </div>
    </section>
    
    <!-- CTA -->
    <section class="cta">
        <h2>Ready to build?</h2>
        <a href="#try-summarize" class="cta-btn">
            Try the API Free
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M5 12h14M12 5l7 7-7 7"/>
            </svg>
        </a>
    </section>
    
    <footer>
        <p>© 2026 Fofo APIs. Built by <a href="https://x.com/Fai9al_fofo">@Fai9al_fofo</a></p>
        <div class="footer-links">
            <a href="#apis">APIs</a>
            <a href="#faq">FAQ</a>
            <a href="#changelog">Changelog</a>
            <a href="https://x.com/Fai9al_fofo">Twitter</a>
        </div>
    </footer>
    
    <script>
        function showTab(btn, tabId) {
            const parent = btn.closest('.code-section');
            parent.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            parent.querySelectorAll('.code-block').forEach(c => c.classList.add('hidden'));
            btn.classList.add('active');
            document.getElementById(tabId).classList.remove('hidden');
        }
        
        async function tryAPI(api, inputId, resultId) {
            const input = document.getElementById(inputId);
            const result = document.getElementById(resultId);
            const btn = input.parentElement.querySelector('.try-btn');
            
            btn.disabled = true;
            btn.textContent = 'Running...';
            result.className = 'try-result show';
            result.textContent = 'Sending request...';
            
            try {
                let body;
                if (api === 'summarize') {
                    body = { text: input.value, max_length: 100 };
                } else if (api === 'validate') {
                    body = { data: input.value };
                }
                
                const response = await fetch('/api/' + api, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(body)
                });
                
                const data = await response.json();
                result.className = 'try-result show ' + (response.ok ? 'success' : 'error');
                result.textContent = JSON.stringify(data, null, 2);
            } catch (err) {
                result.className = 'try-result show error';
                result.textContent = 'Error: ' + err.message;
            }
            
            btn.disabled = false;
            btn.textContent = 'Run Request →';
        }
        
        async function tryOCR() {
            const input = document.getElementById('input_ocr');
            const result = document.getElementById('result_ocr');
            const btn = input.parentElement.querySelector('.try-btn');
            
            btn.disabled = true;
            btn.textContent = 'Running...';
            result.className = 'try-result show';
            result.textContent = 'Processing image...';
            
            try {
                const response = await fetch('/api/ocr', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ image: input.value, language: 'ara' })
                });
                
                const data = await response.json();
                result.className = 'try-result show ' + (data.success ? 'success' : 'error');
                result.textContent = JSON.stringify(data, null, 2);
            } catch (err) {
                result.className = 'try-result show error';
                result.textContent = 'Error: ' + err.message;
            }
            
            btn.disabled = false;
            btn.textContent = 'Run Request →';
        }
        
        // Smooth scroll
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) target.scrollIntoView({ behavior: 'smooth' });
            });
        });
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def root():
    return LANDING_PAGE

@app.get("/api", response_class=HTMLResponse)
def api_root():
    return LANDING_PAGE

@app.get("/api/info")
def api_info():
    return {
        "name": "Fofo APIs",
        "version": "1.0.0",
        "status": "operational",
        "uptime": "99.9%",
        "endpoints": {
            "/api/summarize": {
                "method": "POST",
                "price": "$0.01/req",
                "description": "Summarize Arabic text with AI"
            },
            "/api/validate": {
                "method": "POST", 
                "price": "$0.02/req",
                "description": "Validate emails, phones, URLs"
            },
            "/api/ocr": {
                "method": "POST",
                "price": "$0.01/req",
                "description": "Extract Arabic text from images"
            },
            "/api/convert-image": {
                "method": "POST",
                "price": "$0.01/req",
                "description": "Convert images between formats"
            }
        },
        "rate_limits": {
            "requests_per_minute": 100,
            "requests_per_day": 10000,
            "max_payload_size": "5MB"
        }
    }
