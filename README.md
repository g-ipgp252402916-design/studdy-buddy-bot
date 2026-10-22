# Study Buddy Bot 📚

A simple, **rule-based** chatbot for Gen Z students that teaches effective study habits.  
**No LLM API is used.** Everything runs on keyword matching and predefined intent logic.

---

## 📁 Project Structure

```
study-buddy-bot/
├── bot_engine.py       ← Rule-based engine (shared by web + Telegram)
├── telegram_bot.py     ← Telegram bot runner
├── web/
│   └── index.html      ← Self-contained web interface (open in any browser)
└── README.md
```

---

## ✅ Requirements

| Tool | Minimum Version |
|---|---|
| Python | 3.9+ |
| python-telegram-bot | 20.x |

---

## 🚀 Quick Start

### 1 — Web Interface (no installation required)

Just open `web/index.html` in any modern browser.  
No server, no install, no internet connection needed.

```
study-buddy-bot/web/index.html  ← double-click to open
```

The chatbot runs entirely in the browser using the built-in JavaScript engine.

---

### 2 — Telegram Bot

#### Step 1 — Get a BotFather token

1. Open Telegram and search for **@BotFather**.
2. Send `/newbot` and follow the prompts.
3. Copy the token that looks like:  
   `123456789:ABCdefGHIjklMNOpqrSTUvwxYZ`

#### Step 2 — Install the Python dependency

```bash
pip install python-telegram-bot
```

#### Step 3 — Set your token

**Option A — Environment variable (recommended)**

```bash
# Windows PowerShell
$env:TELEGRAM_BOT_TOKEN = "YOUR_TOKEN_HERE"

# macOS / Linux
export TELEGRAM_BOT_TOKEN="YOUR_TOKEN_HERE"
```

**Option B — Edit the file directly**

Open `telegram_bot.py` and replace the placeholder on this line:

```python
BOT_TOKEN: str = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_BOTFATHER_TOKEN_HERE")
```

#### Step 4 — Run the bot

```bash
cd study-buddy-bot
python telegram_bot.py
```

You should see:

```
INFO | Study Buddy Bot is running… Press Ctrl-C to stop.
```

#### Step 5 — Test in Telegram

1. Search for your bot's username in Telegram.
2. Send `/start` — the bot will greet you with a quick-reply keyboard.
3. Tap any button or type a question freely.

---

## 🧪 Testing the Engine

Run the built-in self-test to verify all intents:

```bash
cd study-buddy-bot
python bot_engine.py
```

Expected output — 14 test inputs each produce a relevant response:

```
============================================================
User : Hi there!
Bot  : Hey there! 👋 I'm Study Buddy Bot...
------------------------------------------------------------
User : Can you give me some tips on how to study better?
Bot  : Of course! 📚 You can improve your study habits by...
...
```

---

## 💬 Supported Intents

| Intent | Example Utterance |
|---|---|
| Greeting | "Hi", "Hello", "Hey" |
| Study Tips | "How do I study better?" |
| Memory Techniques | "How can I remember what I learn?" |
| Study Breaks | "Should I take a break?" |
| Avoiding Distractions | "How do I stay focused?" |
| Study Planning | "Can you help me make a study plan?" |
| Timetable Template | "Show me a timetable template" |
| Note-Taking | "How should I take notes?" |
| Revision | "How do I revise for exams?" |
| Motivation | "I feel like giving up" |
| Sleep & Rest | "How much sleep do I need?" |
| Homework Refusal | "Do my homework for me" |
| Help / Menu | "What can you do?" |
| Goodbye / Thanks | "Thanks!", "Bye!" |

If no intent matches, the bot sends a friendly fallback message.

---

## 🔧 Adding New Intents

Open `bot_engine.py` and add a new entry to the `INTENTS` list:

```python
{
    "name": "my_new_intent",
    "keywords": [r"\bmy keyword\b", r"\banother phrase\b"],
    "responses": [
        "This is the response the bot will give!",
        "This is an alternative response (chosen at random).",
    ],
},
```

Then mirror the same intent inside the `INTENTS` array in `web/index.html`  
(the JS section near the bottom of the file) so the web version stays in sync.

---

## 🌐 Deploying the Web Interface

The web interface is a **single static HTML file** — deploy it anywhere:

| Platform | Steps |
|---|---|
| **GitHub Pages** | Push to a repo → Settings → Pages → select branch/root |
| **Netlify** | Drag and drop the `web/` folder onto netlify.com/drop |
| **Vercel** | `vercel --prod` from the `web/` directory |
| **Any web host** | Upload `index.html` to your public folder |

---

## ☁️ Deploying the Telegram Bot (always-on)

For the bot to respond 24/7 it must run on a server.

**Free options:**
- [Railway.app](https://railway.app) — connect GitHub repo, set `TELEGRAM_BOT_TOKEN` as an env var, deploy.
- [Render.com](https://render.com) — create a "Background Worker", point it at `telegram_bot.py`.
- [PythonAnywhere](https://www.pythonanywhere.com) — upload files, run a "Scheduled task" or "Always-on task".

**Minimum `requirements.txt` for deployment:**

```
python-telegram-bot==20.*
```

---

## ⚠️ Important Restrictions

- The bot will **not** complete homework, assignments, or exams.
- The bot will **not** claim to be a human teacher.
- The bot will **not** answer questions unrelated to studying.
- **No LLM API is used.** All responses are predefined.

---

## 📄 Licence

MIT — free to use, modify, and share.
