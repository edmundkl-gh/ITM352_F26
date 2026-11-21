const $ = (id) => document.getElementById(id);
const screens = ["start-screen", "quiz-screen", "result-screen"];

function show(screen) {
  screens.forEach((s) => ($(s).hidden = s !== screen));
}

function showError(msg) {
  $("error").textContent = msg;
  $("error").hidden = !msg;
}

async function api(path, body) {
  try {
    const res = await fetch(path, body === undefined ? {} : {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Something went wrong.");
    showError("");
    return data;
  } catch (err) {
    showError(err.message || "Network error. Please try again.");
    return null;
  }
}

async function loadLeaderboard() {
  const scores = await api("/api/scores");
  const list = $("leaderboard");
  list.replaceChildren();
  (scores || []).forEach((s) => {
    const li = document.createElement("li");
    li.textContent = `${s.name}: ${s.score}/${s.total} in ${s.seconds}s`;
    list.appendChild(li);
  });
}

async function startQuiz() {
  const data = await api("/api/start", { name: $("name").value });
  if (data) loadQuestion();
}

async function loadQuestion() {
  const q = await api("/api/question");
  if (!q) return;
  if (q.done) return showResult();
  show("quiz-screen");
  $("progress").textContent = `Question ${q.number} of ${q.total}`;
  $("question").textContent = q.question;
  $("feedback").textContent = "";
  $("feedback").className = "";
  $("next-btn").hidden = true;
  const box = $("options");
  box.replaceChildren();
  q.options.forEach((opt) => {
    const b = document.createElement("button");
    b.textContent = opt;
    b.className = "option";
    b.addEventListener("click", () => submitAnswer(opt, b));
    box.appendChild(b);
  });
}

async function submitAnswer(choice, clicked) {
  const r = await api("/api/answer", { choice });
  if (!r) return;
  document.querySelectorAll(".option").forEach((b) => {
    b.disabled = true;
    if (b.textContent === r.correct_answer) b.classList.add("correct");
  });
  if (!r.correct) clicked.classList.add("wrong");
  $("feedback").textContent = r.correct
    ? `Correct! Score: ${r.score}`
    : `Not quite. The answer was ${r.correct_answer}. Score: ${r.score}`;
  $("feedback").className = r.correct ? "good" : "bad";
  $("next-btn").hidden = false;
}

async function showResult() {
  const r = await api("/api/result");
  if (!r) return;
  show("result-screen");
  $("result-title").textContent = `${r.player}, you scored ${r.score} / ${r.total}`;
  const items = [
    `Correct: ${r.correct}`,
    `Incorrect: ${r.incorrect}`,
    `Time taken: ${r.seconds} seconds`,
    r.improve.length ? `Areas to improve: ${r.improve.join(", ")}` : "No weak areas. Nice work!",
  ];
  $("result-details").replaceChildren(...items.map((t) => {
    const li = document.createElement("li");
    li.textContent = t;
    return li;
  }));
}

$("start-btn").addEventListener("click", startQuiz);
$("next-btn").addEventListener("click", loadQuestion);
$("again-btn").addEventListener("click", () => { show("start-screen"); loadLeaderboard(); });
$("name").addEventListener("keydown", (e) => { if (e.key === "Enter") startQuiz(); });

show("start-screen");
loadLeaderboard();