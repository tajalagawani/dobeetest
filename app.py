import os
import openai
import requests
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

N8N_WEBHOOK_URL = "https://dobee.app.n8n.cloud/webhook-test/76eedd64-4c27-4536-a1f9-d1b6952f6f21"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        goals = request.form["goals"]
        progress = request.form["progress"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(goals, progress),
            temperature=1,
            max_tokens=1900,
            top_p=1,
            frequency_penalty=0.1,
            presence_penalty=0.6,
        )
        suggestions = response.choices[0].text
        send_to_n8n(suggestions)
        return redirect(url_for("index", result=suggestions))

    result = request.args.get("result")
    return render_template("index.html", result=result)

def generate_prompt(goals, progress):
    return f""" write me 10 recommended  goal thaf if i make it will help me to achieve my goal on the following input , write the answer to Norwegian i want use it on my OKR system

Current Goals: {goals}
Progress Made: {progress}

New Goals: """

import json

import json
import os


def send_to_n8n(suggestions):
    suggestions_list = suggestions.split("\n")
    data = {"results": "\n".join(suggestions_list)}
    response = requests.post(N8N_WEBHOOK_URL, json=data)
    if response.status_code == 200:
        print("Results sent to N8N successfully!")
    else:
        print("Error sending results to N8N")


if __name__ == "__main__":
    app.run(debug=False)
