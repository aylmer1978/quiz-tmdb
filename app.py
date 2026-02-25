from flask import Flask, render_template, jsonify
from tmdb_client import generate_question

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/question')
def get_question():
    question_data = generate_question()
    if question_data:
        return jsonify(question_data)
    return jsonify({"error": "Could not generate question"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
