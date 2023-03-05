import os
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        goals = request.form["goals"]
        progress = request.form["progress"]
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=generate_prompt(goals, progress),
            temperature=0.5,
            max_tokens=50,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)

def generate_prompt(goals, progress):
    return f""" Generate 10 goal to achieve my goal on the following input , and translate them into Norwegian.

Current Goals: {goals}
Progress Made: {progress}

New Goals: """

if __name__ == "__main__":
    app.run(debug=True)
