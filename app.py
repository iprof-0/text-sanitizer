import sys
import re
import threading
import webbrowser
import time
from flask import Flask, request, render_template_string

# Initialize Flask App
app = Flask(__name__)

# Single File Template with Cyber Theme
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>String Sanitizer Tool</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        /* =========================================
           VARIABLES & RESET (Cyber Theme)
           ========================================= */
        :root {
            --bg-dark: #0a0a0a;
            --bg-card: #111111;
            --bg-card-hover: #161616;
            
            --primary: #00ff88;       /* Neon Green */
            --primary-dim: rgba(0, 255, 136, 0.1);
            --secondary: #00ccff;     /* Cyan */
            --accent: #ff0055;        /* Red */
            
            --text-main: #e0e0e0;
            --text-muted: #a0a0a0;
            
            --border-color: rgba(255, 255, 255, 0.08);
            
            --font-main: 'Inter', sans-serif;
            --font-code: 'JetBrains Mono', monospace;
            
            --transition: all 0.3s ease;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: var(--font-main);
            background-color: var(--bg-dark);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(0, 255, 136, 0.03), transparent 25%),
                radial-gradient(circle at 85% 30%, rgba(0, 204, 255, 0.03), transparent 25%);
        }

        /* =========================================
           LAYOUT & COMPONENTS
           ========================================= */
        .container {
            width: 100%;
            max-width: 700px;
            padding: 20px;
        }

        /* Card Style */
        .cyber-card {
            background: var(--bg-card);
            padding: 40px;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
            transition: var(--transition);
        }

        .cyber-card:hover {
            border-color: var(--primary);
            box-shadow: 0 20px 50px rgba(0, 255, 136, 0.05);
        }

        /* Typography */
        h1 {
            font-family: var(--font-code);
            color: #fff;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2rem;
            letter-spacing: -1px;
        }

        .subtitle {
            text-align: center;
            color: var(--text-muted);
            margin-bottom: 30px;
            font-size: 0.95rem;
        }

        .highlight { color: var(--primary); }

        /* Forms */
        .form-group {
            margin-bottom: 25px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-family: var(--font-code);
            font-size: 0.85rem;
            color: var(--primary);
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        textarea, input[type="text"] {
            width: 100%;
            background-color: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border-color);
            color: var(--text-main);
            padding: 15px;
            border-radius: 6px;
            font-family: var(--font-main);
            font-size: 1rem;
            transition: var(--transition);
        }

        textarea:focus, input:focus {
            outline: none;
            border-color: var(--primary);
            background-color: rgba(0, 255, 136, 0.02);
            box-shadow: 0 0 15px var(--primary-dim);
        }

        textarea {
            min-height: 120px;
            resize: vertical;
        }

        /* Buttons */
        .btn {
            width: 100%;
            padding: 15px;
            background: var(--primary-dim);
            color: var(--primary);
            border: 1px solid var(--primary);
            border-radius: 4px;
            font-family: var(--font-code);
            font-weight: 700;
            text-transform: uppercase;
            cursor: pointer;
            transition: var(--transition);
            letter-spacing: 1px;
        }

        .btn:hover {
            background: var(--primary);
            color: #000;
            box-shadow: 0 0 20px var(--primary-dim);
        }

        /* Results Area */
        .result-container {
            margin-top: 30px;
            padding-top: 30px;
            border-top: 1px solid var(--border-color);
            animation: fadeIn 0.5s ease;
        }

        .result-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }

        .result-box {
            background: #050505;
            padding: 20px;
            border-radius: 6px;
            border: 1px solid var(--border-color);
            font-family: var(--font-code);
            color: var(--text-main);
            white-space: pre-wrap;
            word-break: break-word;
        }

        .copy-btn {
            background: transparent;
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 5px 15px;
            border-radius: 4px;
            cursor: pointer;
            font-family: var(--font-code);
            font-size: 0.8rem;
            transition: var(--transition);
        }

        .copy-btn:hover {
            color: var(--primary);
            border-color: var(--primary);
        }

        /* Footer */
        .footer {
            margin-top: 40px;
            text-align: center;
            font-size: 0.85rem;
            color: var(--text-muted);
        }

        .footer a {
            color: var(--text-muted);
            text-decoration: none;
            transition: var(--transition);
            font-weight: 600;
        }

        .footer a:hover {
            color: var(--primary);
        }

        /* Error */
        .error-msg {
            color: var(--accent);
            background: rgba(255, 0, 85, 0.1);
            border: 1px solid rgba(255, 0, 85, 0.2);
            padding: 15px;
            border-radius: 6px;
            margin-top: 20px;
            font-size: 0.9rem;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>

    <div class="container">
        <div class="cyber-card">
            <h1>TEXT <span class="highlight">SANITIZER</span></h1>
            <p class="subtitle">Securely remove specific patterns from your text.</p>

            <form method="POST">
                <div class="form-group">
                    <label for="sentence">Source Text</label>
                    <textarea id="sentence" name="sentence" placeholder="Paste your source text here..." required autofocus>{{ original_text if original_text else '' }}</textarea>
                </div>
                
                <div class="form-group">
                    <label for="word">Target String</label>
                    <input type="text" id="word" name="word" placeholder="e.g. SensitiveData" required value="{{ target_word if target_word else '' }}">
                </div>
                
                <button type="submit" class="btn">Process Text</button>
            </form>

            {% if error %}
                <div class="error-msg">
                    <strong>Error:</strong> {{ error }}
                </div>
            {% endif %}

            {% if result %}
                <div class="result-container">
                    <div class="result-header">
                        <label>Cleaned Output</label>
                        <button class="copy-btn" onclick="copyToClipboard(this)">Copy Output</button>
                    </div>
                    <div class="result-box" id="result-text">{{ result }}</div>
                </div>
            {% endif %}
        </div>

        <div class="footer">
            Designed & Built by <a href="https://iprof-0.github.io/Zero/#contact" target="_blank">Zero</a>
        </div>
    </div>

    <script>
        function copyToClipboard(btn) {
            const text = document.getElementById('result-text').innerText;
            navigator.clipboard.writeText(text).then(() => {
                const originalText = btn.innerText;
                btn.innerText = "COPIED!";
                btn.style.color = "var(--primary)";
                btn.style.borderColor = "var(--primary)";
                
                setTimeout(() => {
                    btn.innerText = originalText;
                    btn.style.color = "";
                    btn.style.borderColor = "";
                }, 2000);
            });
        }
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    error = None
    original_text = ""
    target_word = ""

    if request.method == 'POST':
        original_text = request.form.get('sentence', '')
        target_word = request.form.get('word', '')

        # Validation
        if not original_text or not target_word:
             error = "Input data is missing."
        else:
            # Logic: Case insensitive removal
            try:
                modified_sentence = re.sub(
                    re.escape(target_word), 
                    '', 
                    original_text, 
                    flags=re.IGNORECASE
                )
                result = modified_sentence
            except Exception as e:
                error = f"System Error: {str(e)}"

    return render_template_string(
        HTML_TEMPLATE, 
        result=result, 
        error=error,
        original_text=original_text,
        target_word=target_word
    )

def open_browser():
    """Opens browser automatically"""
    time.sleep(1.5)
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    # Threading for browser
    threading.Thread(target=open_browser).start()
    
    # Run Flask
    app.run(port=5000, debug=False)
