import json
import os
from flask import Flask, render_template, jsonify, request
from tmdb_client import generate_question

app = Flask(__name__)
RANKING_FILE = 'ranking.json'

def load_ranking():
    if os.path.exists(RANKING_FILE):
        with open(RANKING_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_ranking(ranking):
    with open(RANKING_FILE, 'w', encoding='utf-8') as f:
        json.dump(ranking, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/question')
def get_question():
    question_data = generate_question()
    if question_data:
        return jsonify(question_data)
    return jsonify({"error": "Could not generate question"}), 500

@app.route('/api/ranking', methods=['GET'])
def get_ranking():
    return jsonify(load_ranking())

@app.route('/api/ranking', methods=['POST'])
def add_score():
    data = request.json
    name = data.get('name', 'Anónimo')[:20] # Limitar longitud
    score = data.get('score', 0)
    
    ranking = load_ranking()
    ranking.append({"name": name, "score": score})
    # Ordenar por puntuación descendente y mantener solo el top 10
    ranking = sorted(ranking, key=lambda x: x['score'], reverse=True)[:10]
    
    save_ranking(ranking)
    return jsonify(ranking)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
