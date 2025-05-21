// Experimental mini-game
// ---------------------
// This file powers the "Guess That Persona" browser game. The game lives in its
// own folder and is **not integrated** with the main GPT Frenzy app. It may
// change or be removed in future updates.

const personas = [
  {
    name: "Mimi",
    blurb: "Warm, concise, art-director vibe",
    answers: [
      "Sure thing—let’s simplify that color palette first.",
      "Clip the mid-tones, then push the highlights. Easy win.",
      "Picture a soft-focus lens and blush-pink neon—boom, cover shot!",
    ],
  },
  {
    name: "Supernova",
    blurb: "Bold, gangsta-cyberpunk critic",
    answers: [
      "Yo, ditch the grayscale—go full chroma or go home.",
      "Not gonna lie, that skyline’s lookin’ thirsty for lasers.",
      "Slap a glitch overlay, crank the bass, and watch it pop.",
    ],
  },
  {
    name: "BlckButterfly",
    blurb: "Poetic, introspective sage",
    answers: [
      "Every pixel is a cocoon—let it breathe into bloom.",
      "The canvas hums; add silence, and you’ll hear wings.",
      "Shadow is merely light resting—paint its dreams.",
    ],
  },
];

const qs = [
  "How would you improve this design mock-up?",
  "Any quick lighting tips?",
  "Describe an epic futuristic outfit.",
  "Make this skyline pop.",
  "How do I handle creative block?",
];

let score = 0,
  round = 0,
  locked = false;

const $app = document.getElementById("app"),
  $score = document.getElementById("score");

nextRound();

function showMessage(msg) {
  const box = document.getElementById("feedback");
  if (box) box.textContent = msg;
}

function nextRound() {
  locked = false;
  if (round === 5) {
    $score.textContent = `${score}/5`;
    $app.innerHTML = `<h2>Game over! ${score}/5 🎉</h2>`;
    return;
  }
  round++;
  $score.textContent = `${score}/${round - 1}`;
  const q = qs[Math.floor(Math.random() * qs.length)];
  const picks = shuffle(personas.slice());
  const target = picks[Math.floor(Math.random() * picks.length)];
  $app.innerHTML = `<h2>Round ${round}: Pick <span style="color:#0f0">${target.name}</span>'s reply</h2><p>${q}</p><p id="feedback"></p>`;

  picks.forEach((p) => {
    const a = p.answers[Math.floor(Math.random() * p.answers.length)];
    const btn = document.createElement("button");
    btn.textContent = a;
    $app.appendChild(btn);
    btn.onclick = () => {
      if (locked) return;
      locked = true;
      $app.querySelectorAll("button").forEach((b) => (b.disabled = true));
      if (p === target) {
        score++;
        showMessage(`✅ Correct! ${p.blurb}`);
      } else {
        showMessage(`❌ Nope – that was ${p.name}`);
      }
      $score.textContent = `${score}/${round}`;
      setTimeout(nextRound, 800);
    };
  });
}

function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}
