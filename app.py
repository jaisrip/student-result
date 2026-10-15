
from flask import Flask, request
import joblib
import os

app = Flask(__name__)
model = joblib.load("model.pkl")
VERSION = os.getenv("MODEL_VERSION", "1.0")

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""

    if request.method == "POST":
        try:
            hours = float(request.form["hours"])
            attendance = float(request.form["attendance"])
            marks = float(request.form["marks"])

            if not (0 <= hours <= 10 and
                    0 <= attendance <= 100 and
                    0 <= marks <= 100):
                raise ValueError()

            prediction = model.predict(
                [[hours, attendance, marks]]
            )[0]

            result = "Pass" if prediction == 1 else "Fail"

        except (ValueError, TypeError):
            result = "Enter valid values within the allowed ranges."

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Student Result Predictor</title>
        <style>
            body {font-family: Arial; margin: 50px auto;
                  max-width: 420px; padding: 20px;}
            input, button {padding: 10px; margin: 8px 0;
                           width: 100%; box-sizing: border-box;}
        </style>
    </head>
    <body>
        <h2>Student Result Predictor</h2>
        <p>Model Version: """ + VERSION + """</p>
        <form method="POST">
            Study Hours (0-10):
            <input type="number" name="hours"
                   min="0" max="10" step="any" required>
            Attendance % (0-100):
            <input type="number" name="attendance"
                   min="0" max="100" step="any" required>
            Internal Marks (0-100):
            <input type="number" name="marks"
                   min="0" max="100" step="any" required>
            <button type="submit">Predict Result</button>
        </form>
        <h3>Prediction: """ + result + """</h3>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)