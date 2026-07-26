import os
from flask import Flask, request, render_template_string
import google.generativeai as genai

app = Flask(__name__)

# Read the Gemini API key from an environment variable (set via Docker / GitHub secret, never hard-coded)
API_KEY = os.environ.get("GEMINI_API_KEY", "")

model = None
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-3.5-flash")

PAGE = """
<!DOCTYPE html>
<html>
<head>
  <title>DevOps AI Assistant</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; background:#0f172a; color:#e2e8f0; }
    h1 { color: #38bdf8; }
    textarea, input { width: 100%; padding: 10px; margin-top: 8px; border-radius: 6px; border: none; box-sizing: border-box; }
    button { margin-top: 12px; padding: 10px 20px; background:#38bdf8; border:none; border-radius:6px; cursor:pointer; font-weight:bold; }
    .answer { background:#1e293b; padding:16px; border-radius:8px; margin-top:20px; white-space: pre-wrap; }
    .error { color: #f87171; }
  </style>
</head>
<body>
  <h1>DevOps AI Assistant</h1>
  <p>Ask a DevOps / Cloud question, or paste a log to analyze.</p>
  <form method="POST">
    <textarea name="question" rows="6" placeholder="Ask a question OR paste a log here...">{{ question or '' }}</textarea>
    <button type="submit">Ask AI</button>
  </form>
  {% if answer %}
  <div class="answer"><b>AI Response:</b><br>{{ answer }}</div>
  {% endif %}
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    answer = None
    question = None

    if request.method == "POST":
        question = request.form.get("question", "")

        if not API_KEY or model is None:
            answer = "ERROR: GEMINI_API_KEY is not set on the server."
        elif question.strip():
            prompt = (
                "You are a helpful, concise DevOps and Cloud expert assistant. "
                "If the user pastes a log, find errors and suggest fixes. "
                "If they ask a question, answer clearly for a beginner.\n\n" + question
            )
            try:
                result = model.generate_content(prompt)
                answer = result.text
            except Exception as e:
                answer = "AI request failed: " + str(e)

    return render_template_string(PAGE, answer=answer, question=question)


@app.route("/health")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
