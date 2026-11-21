import json
import random
import re
import time
from datetime import timedelta
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, session, jsonify

BASE_DIR = Path(__file__).parent
QUESTIONS_FILE = BASE_DIR / "data" / "questions.json"
SCORES_FILE = BASE_DIR / "scores.json"
NAME_PATTERN = re.compile(r"^[A-Za-z0-9 _'-]{1,30}$")
WEAK_THRESHOLD = 0.7  # categories scored below this show up as "areas to improve"
LOAD_ERROR = "Sorry, the quiz questions could not be loaded. Please try again later."

app = Flask(__name__)
app.secret_key = "change-me-before-deploying"
app.permanent_session_lifetime = timedelta(days=365)


# ---------- data helpers ----------

def load_questions():
    """Return {id: question} from the JSON file, or None if it can't be read."""
    try:
        with open(QUESTIONS_FILE, encoding="utf-8") as f:
            questions = json.load(f)
        for q in questions:
            if q["answer"] not in q["options"]:
                return None
        return {q["id"]: q for q in questions}
    except (OSError, ValueError, KeyError, TypeError):
        return None


def load_scores():
    try:
        with open(SCORES_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return []


def save_score(entry):
    scores = load_scores()
    scores.append(entry)
    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2)


def top_scores(limit=10):
    return sorted(load_scores(), key=lambda s: (-s["score"], s["seconds"]))[:limit]


def player_scores(name):
    if not name:
        return []
    return [score for score in load_scores()
            if score.get("name", "").casefold() == name.casefold()]


def render_index(error=None, selected_category="All categories"):
    questions = load_questions()
    if questions is None:
        error = error or LOAD_ERROR
        categories = []
    else:
        categories = sorted({q["category"] for q in questions.values()})
    player = session.get("player")
    return render_template("index.html", error=error, scores=top_scores(5),
                           player=player, user_scores=player_scores(player),
                           categories=categories,
                           selected_category=selected_category)


# ---------- page routes ----------

@app.route('/')
def index():
    return render_index()


@app.route('/start', methods=['POST'])
def start():
    name = request.form.get('name', '').strip() or session.get('player', '')
    category = request.form.get('category', 'All categories')
    if not NAME_PATTERN.match(name):
        return render_index(
            "Name must be 1-30 characters: letters, numbers, spaces, - _ '",
            category)
    questions = load_questions()
    if questions is None:
        return render_index(LOAD_ERROR)

    categories = {q["category"] for q in questions.values()}
    if category != "All categories" and category not in categories:
        return render_index("Please select a valid quiz category.")
    if category != "All categories":
        questions = {qid: q for qid, q in questions.items()
                     if q["category"] == category}

    session.clear()
    session['player'] = name
    session.permanent = True
    session['category'] = category
    session['order'] = random.sample(list(questions), len(questions))  # random question order
    session['question_number'] = 0
    session['score'] = 0
    session['answers'] = []
    session['options'] = None
    session['feedback'] = None
    session['started'] = time.time()
    session['finished'] = None
    session['saved'] = False
    return redirect(url_for('quiz'))


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'order' not in session:
        return redirect(url_for('index'))
    questions = load_questions()
    if questions is None:
        return render_index(LOAD_ERROR)

    n = session['question_number']
    if n >= len(session['order']):
        return redirect(url_for('result'))

    q = questions[session['order'][n]]
    if session['options'] is None:  # shuffle once so a refresh keeps the same order
        session['options'] = random.sample(q['options'], len(q['options']))

    error = None
    if request.method == 'POST':
        answer = request.form.get('answer')
        if answer not in session['options']:
            error = "Please select an answer before submitting."
        else:
            correct = (answer == q['answer'])
            session['answers'] = session['answers'] + [
                {"category": q['category'], "correct": correct}]
            session['score'] += 1 if correct else 0
            session['feedback'] = {"correct": correct, "your_answer": answer,
                                   "correct_answer": q['answer']}
            session['question_number'] = n + 1
            session['options'] = None
            if n + 1 == len(session['order']):
                session['finished'] = time.time()
            return redirect(url_for('feedback'))  # Post/Redirect/Get

    return render_template('quiz.html', question=q['question'],
                           question_number=n, options=session['options'], error=error)


@app.route('/feedback')
def feedback():
    if 'order' not in session or session.get('feedback') is None:
        return redirect(url_for('quiz'))
    finished = session['question_number'] >= len(session['order'])
    return render_template('feedback.html', feedback=session['feedback'],
                           score=session['score'], finished=finished)


@app.route('/result')
def result():
    if 'order' not in session:
        return redirect(url_for('index'))
    if session['finished'] is None:
        return redirect(url_for('quiz'))

    answers = session['answers']
    score = session['score']
    by_category = {}
    for a in answers:
        c = by_category.setdefault(a['category'], {"correct": 0, "total": 0})
        c['total'] += 1
        c['correct'] += 1 if a['correct'] else 0
    improve = [c for c, v in by_category.items() if v['correct'] / v['total'] < WEAK_THRESHOLD]
    seconds = round(session['finished'] - session['started'], 1)

    if not session['saved']:  # don't double-save on refresh
        selected_category = session.get('category', 'All categories')
        save_score({"name": session['player'], "score": score,
                    "total": len(answers), "seconds": seconds,
                    "category": selected_category})
        session['saved'] = True
    else:
        selected_category = session.get('category', 'All categories')

    return render_template('results.html', score=score, max_questions=len(answers),
                           incorrect=len(answers) - score, seconds=seconds,
                           by_category=by_category, improve=improve,
                           selected_category=selected_category)


# ---------- REST API ----------

@app.route('/api/questions')
def api_questions():
    """All questions, WITHOUT the answers."""
    questions = load_questions()
    if questions is None:
        return jsonify(error=LOAD_ERROR), 500
    return jsonify([{"id": q["id"], "category": q["category"],
                     "question": q["question"], "options": q["options"]}
                    for q in questions.values()])


@app.route('/api/scores', methods=['GET'])
def api_get_scores():
    return jsonify(top_scores())


@app.route('/api/scores', methods=['POST'])
def api_post_scores():
    data = request.get_json(silent=True) or {}
    name = str(data.get('name', '')).strip()
    score, total, seconds = data.get('score'), data.get('total'), data.get('seconds')
    if not NAME_PATTERN.match(name):
        return jsonify(error="Invalid name."), 400
    if not all(isinstance(v, int) and not isinstance(v, bool) for v in (score, total)) \
            or not isinstance(seconds, (int, float)) or not 0 <= score <= total:
        return jsonify(error="score and total must be integers with 0 <= score <= total, "
                             "and seconds must be a number."), 400
    save_score({"name": name, "score": score, "total": total, "seconds": seconds})
    return jsonify(saved=True), 201


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()