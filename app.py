# app.py
from flask import Flask, render_template, request, jsonify
import requests
import openai
from config import RECAPTCHA_SECRET_KEY, OPENAI_API_KEY

app = Flask(__name__)
openai.api_key = OPENAI_API_KEY

def verify_recaptcha(token):
    url = "https://www.google.com/recaptcha/api/siteverify"
    data = {"secret": RECAPTCHA_SECRET_KEY, "response": token}
    response = requests.post(url, data=data)
    return response.json().get("success", False)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    recaptcha_token = request.form.get("g-recaptcha-response")
    user_message = request.form.get("message")

    if not verify_recaptcha(recaptcha_token):
        return jsonify({"error": "reCAPTCHA failed. Please try again."})

    response_text = generate_response(user_message)
    return jsonify({"response": response_text})

def generate_response(message):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=message,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    app.run(debug=True)
