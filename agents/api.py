from flask import Flask, request, jsonify
from app import run_system

app = Flask(__name__)

@app.route("/run", methods=["POST"])
def run():
    data = request.json
    result = run_system(data["text"])
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)