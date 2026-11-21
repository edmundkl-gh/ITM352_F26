import json
import pytest
import app as quiz_app

QUESTIONS = [
    {"id": 1, "category": "Geo", "question": "Capital of France?",
     "options": ["Madrid", "Paris"], "answer": "Paris"},
    {"id": 2, "category": "Sci", "question": "Red planet?",
     "options": ["Mars", "Venus"], "answer": "Mars"},
]


@pytest.fixture
def client(tmp_path, monkeypatch):
    qfile = tmp_path / "q.json"
    qfile.write_text(json.dumps(QUESTIONS))
    monkeypatch.setattr(quiz_app, "QUESTIONS_FILE", qfile)
    monkeypatch.setattr(quiz_app, "SCORES_FILE", tmp_path / "scores.json")
    quiz_app.app.config["TESTING"] = True
    return quiz_app.app.test_client()


def play(client, correct=True):
    client.post("/start", data={"name": "Ed"})
    answers = {q["id"]: q["answer"] for q in QUESTIONS}
    for _ in QUESTIONS:
        client.get("/quiz")
        with client.session_transaction() as s:
            qid = s["order"][s["question_number"]]
            options = s["options"]
        right = answers[qid]
        choice = right if correct else next(o for o in options if o != right)
        client.post("/quiz", data={"answer": choice})


def test_bad_name_rejected(client):
    r = client.post("/start", data={"name": "<script>"})
    assert b"Name must be" in r.data


def test_quiz_requires_start(client):
    assert client.get("/quiz").status_code == 302


def test_home_page_lists_quiz_categories(client):
    response = client.get("/")
    assert b'value="All categories"' in response.data
    assert b'value="Geo"' in response.data
    assert b'value="Sci"' in response.data


def test_selected_category_limits_questions_and_score_summary(client):
    client.post("/start", data={"name": "Ed", "category": "Sci"})
    with client.session_transaction() as user_session:
        assert len(user_session["order"]) == 1
        assert user_session["category"] == "Sci"

    client.get("/quiz")
    with client.session_transaction() as user_session:
        question_id = user_session["order"][user_session["question_number"]]
        question = next(q for q in QUESTIONS if q["id"] == question_id)
        options = user_session["options"]
    client.post("/quiz", data={"answer": question["answer"]})

    response = client.get("/result")
    assert b"Category selected: Sci" in response.data
    assert b"Sci: 1 / 1" in response.data
    assert b"Geo:" not in response.data


def test_invalid_category_is_rejected(client):
    response = client.post(
        "/start", data={"name": "Ed", "category": "Unknown"})
    assert b"valid quiz category" in response.data


def test_first_visit_asks_for_name(client):
    response = client.get("/")
    assert b"First visit?" in response.data
    assert b'name="name"' in response.data


def test_returning_player_sees_own_score_history(client):
    play(client)
    client.get("/result")

    response = client.get("/")
    assert b"Welcome back, Ed!" in response.data
    assert b"Your score history" in response.data
    assert b"/2 in " in response.data
    with client.session_transaction() as user_session:
        assert user_session["player"] == "Ed"
        assert user_session.permanent


def test_player_score_history_is_private_to_session_name(client):
    client.post("/api/scores", json={
        "name": "Other", "score": 2, "total": 2, "seconds": 1
    })
    client.post("/start", data={"name": "Ed"})

    response = client.get("/")
    assert b"Welcome back, Ed!" in response.data
    assert b"You haven't completed a quiz yet." in response.data


def test_missing_answer_does_not_advance(client):
    client.post("/start", data={"name": "Ed"})
    r = client.post("/quiz", data={})
    assert b"select an answer" in r.data
    with client.session_transaction() as s:
        assert s["question_number"] == 0


def test_perfect_score(client):
    play(client, correct=True)
    assert b"2 out of 2" in client.get("/result").data


def test_score_saved_once(client):
    play(client)
    client.get("/result")
    client.get("/result")
    assert len(client.get("/api/scores").get_json()) == 1


def test_all_wrong_flags_both_categories(client):
    play(client, correct=False)
    data = client.get("/result").data
    assert b"0 out of 2" in data and b"Geo" in data and b"Sci" in data


def test_api_questions_hide_answers(client):
    qs = client.get("/api/questions").get_json()
    assert len(qs) == 2 and all("answer" not in q for q in qs)


def test_bundled_questions_load():
    response = quiz_app.app.test_client().get("/api/questions")
    assert response.status_code == 200
    questions = response.get_json()
    assert len(questions) == 9
    assert all("answer" not in question for question in questions)
    assert {question["category"] for question in questions} >= {
        "Science", "History", "Sports"
    }


def test_api_post_score_validation(client):
    bad = client.post("/api/scores", json={"name": "Ed", "score": 5, "total": 2, "seconds": 3})
    assert bad.status_code == 400
    good = client.post("/api/scores", json={"name": "Ed", "score": 2, "total": 2, "seconds": 3})
    assert good.status_code == 201