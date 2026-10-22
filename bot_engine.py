"""
Study Buddy Bot — Rule-Based Chatbot Engine
No LLM API. Uses keyword matching and intent recognition.
"""

import re
import random
from typing import Optional

# ─────────────────────────────────────────────
# INTENT DEFINITIONS
# Each intent has:
#   keywords  – list of regex-compatible patterns
#   responses – list of possible replies (one is chosen at random)
# ─────────────────────────────────────────────
INTENTS = [
    {
        "name": "greeting",
        "keywords": [
            r"\bhello\b", r"\bhi\b", r"\bhey\b", r"\bgood morning\b",
            r"\bgood afternoon\b", r"\bgood evening\b", r"\bsup\b",
        ],
        "responses": [
            "Hey there! 👋 I'm Study Buddy Bot. I'm here to help you build great study habits. What would you like to know today?",
            "Hello! 😊 Welcome to Study Buddy Bot! Ask me anything about study tips, time management, memory tricks, and more.",
        ],
    },
    {
        "name": "general_study_tips",
        "keywords": [
            r"\bstudy tips?\b",                  # "study tip" / "study tips"
            r"\beffective study",                 # "effective study techniques"
            r"\bstudy technique",                 # "study techniques"
            r"\btips.*study",                     # "tips on how to study"
            r"\bhelp me study\b",                 # "help me study"
            r"\bhow do i study\b",
            r"\bwhat are.*study",                 # "what are some study tips"
        ],
        "responses": [
            (
                "Here are some practical study tips! 📚\n\n"
                "  🎯  Set clear study goals before each session\n"
                "  🏡  Choose a quiet, tidy space with no distractions\n"
                "  🔁  Use active recall — test yourself instead of just re-reading\n"
                "  📅  Review your lessons regularly, not just before exams\n"
                "  ✏️  Take concise notes and rewrite them in your own words\n\n"
                "Consistent daily effort beats last-minute cramming every time! 💪"
            ),
        ],
    },
    {
        "name": "improve_study_habits",
        "keywords": [
            r"\bimprove.*study habit",            # "improve my study habits"
            r"\bstudy better\b",                  # "how can I study better"
            r"\bhow to study better\b",
            r"\bimprove.*studying\b",             # "improve my studying"
            r"\bbetter student\b",
            r"\blearn better\b",
            r"\blearn faster\b",
            r"\bbuild.*study",                    # "build a study routine"
            r"\bstudy routine\b",
            r"\bstudy habit\b",
        ],
        "responses": [
            (
                "Building strong study habits takes consistency — here's how! 📈\n\n"
                "  🗓️  Follow a daily study routine at the same time each day\n"
                "  🎯  Set small, realistic goals (e.g. 'finish one chapter today')\n"
                "  ✅  Track your daily progress in a journal or app\n"
                "  🔄  Review what you studied the day before at the start of each session\n"
                "  🏆  Reward yourself for hitting weekly milestones\n\n"
                "Small consistent steps build lasting habits. You've got this! 😊"
            ),
        ],
    },
    {
        "name": "memory_techniques",
        "keywords": [
            r"\bremember\b",
            r"\bmemorize\b",
            r"\bmemory\b",                        # "improve my memory", "memory techniques"
            r"\bforget\b",
            r"\bretain\b",
            r"\brecall\b",
            r"\bflashcard\b",
            r"\bmind map\b",
            r"\bspaced repetition\b",
            r"\bactive recall\b",
        ],
        "responses": [
            (
                "Great question! 🧠 Here are some proven memory techniques:\n\n"
                "  🃏  Flashcards — write a question on one side, the answer on the other, and test yourself\n"
                "  🔁  Active recall — close your notes and try to recall the key points from memory\n"
                "  ⏳  Spaced repetition — review material after 1 day, 3 days, then 1 week\n"
                "  🗺️  Mind maps — draw visual diagrams to connect related ideas\n"
                "  ✍️  Teach it — explain what you've learned to someone else (or even to yourself)\n\n"
                "Which technique would you like to try first?"
            ),
        ],
    },
    {
        "name": "breaks",
        "keywords": [
            r"\bbreaks?\b",              # "break" or "breaks"
            r"\bpomodoro\b",
            r"\brest\b",
            r"\bhow long.*study\b",
            r"\bstudy.*hour\b",
            r"\btired\b",
            r"\bburnout\b",
            r"\bexhausted\b",
        ],
        "responses": [
            (
                "Taking breaks is super important! ⏱️\n"
                "Try the Pomodoro Technique:\n"
                "  ✅  Study for 25 minutes\n"
                "  ✅  Rest for 5 minutes\n"
                "  ✅  After 4 rounds, take a longer 15–30 min break\n\n"
                "Adjust the timing to suit your needs. Your brain needs rest to absorb information! 💡"
            ),
        ],
    },
    {
        "name": "distractions",
        "keywords": [
            r"\bdistract",               # "distract", "distracting", "distractions"
            r"\bphone\b",
            r"\bsocial media\b",
            r"\bfocus\b",
            r"\bconcentrat",             # "concentrate", "concentrating"
            r"\bnotification\b",
            r"\bnoisy\b",
            r"\bquiet\b",
            r"\benvironment\b",
        ],
        "responses": [
            (
                "Staying focused is a skill you can practise! 🎯 Here are some tips:\n"
                "  📵  Put your phone face-down or in another room\n"
                "  🔕  Turn off unnecessary notifications\n"
                "  🏡  Study in a quiet, tidy space\n"
                "  🎯  Set ONE small goal for each study session\n"
                "  🎧  Try lo-fi or white-noise music if silence is too hard\n\n"
                "Small changes make a big difference!"
            ),
        ],
    },
    {
        "name": "study_plan",
        "keywords": [
            r"\bstudy plan\b", r"\btimetable\b", r"\bschedule\b",
            r"\bplan.*study\b", r"\borganize\b", r"\borganise\b",
            r"\btime manag\b", r"\bplan.*time\b",
        ],
        "responses": [
            (
                "A good study plan keeps you on track! 📅 Here's how to make one:\n"
                "  1️⃣  List all your subjects\n"
                "  2️⃣  Find out your exam or assignment dates\n"
                "  3️⃣  Decide how many hours per week you can study\n"
                "  4️⃣  Spread subjects evenly across the week\n"
                "  5️⃣  Include breaks and fun time too!\n\n"
                "Would you like a simple weekly timetable template? Just ask! 📋"
            ),
        ],
    },
    {
        "name": "timetable_template",
        "keywords": [
            r"\btemplate\b", r"\bexample timetable\b", r"\bsample.*schedule\b",
            r"\bgive.*timetable\b", r"\bshow.*timetable\b",
        ],
        "responses": [
            (
                "Here's a simple weekly template you can adapt! 🗓️\n\n"
                "```\n"
                "Mon: Maths (1 hr) | English (30 min)\n"
                "Tue: Science (1 hr) | Review Monday notes (20 min)\n"
                "Wed: History (1 hr) | Flashcard revision (20 min)\n"
                "Thu: Maths (1 hr) | Free reading (30 min)\n"
                "Fri: Full review of the week (1 hr)\n"
                "Sat: Light revision + Rest\n"
                "Sun: Rest & recharge 🔋\n"
                "```\n"
                "Adjust subjects and times to match your own timetable. Consistency beats cramming! 💪"
            ),
        ],
    },
    {
        "name": "notes",
        "keywords": [
            r"\bnotes?\b",               # "note" or "notes"
            r"\bnote.?tak",              # "note-taking", "notetaking"
            r"\bbetter notes?\b",        # "take better notes"
            r"\bwrite down\b",
            r"\bjot\b",
            r"\bsummariz",
            r"\bhighlight\b",
            r"\bcornell\b",
        ],
        "responses": [
            (
                "Taking great notes helps you remember more! ✏️ Try these methods:\n"
                "  📝  Cornell Notes – divide your page into notes, cues, and summary\n"
                "  🗒️  Bullet points – keep it short and clear\n"
                "  🖊️  Highlight key ideas, not everything\n"
                "  🔄  Rewrite your notes in your own words after class\n\n"
                "The act of rewriting is powerful — it helps your brain store the information!"
            ),
        ],
    },
    {
        "name": "revision",
        "keywords": [
            r"\brevise\b",
            r"\brevision\b",
            r"\bexam prep\b",
            r"\bprepare.*exam",          # "prepare for my exams"
            r"\bexam.*prep",             # "exam preparation"
            r"\bprepare.*test\b",
            r"\btest prep\b",
            r"\bpractice question\b",
            r"\bpast paper\b",
            r"\bquiz\b",
        ],
        "responses": [
            (
                "Smart revision makes a huge difference! 📖 Here's how to revise effectively:\n"
                "  🔁  Use spaced repetition – review material after 1 day, 3 days, 1 week\n"
                "  📝  Do practice questions and past papers\n"
                "  🤔  Test yourself without looking at your notes first\n"
                "  👥  Study with a friend and quiz each other\n\n"
                "Don't just re-read — actively test your knowledge!"
            ),
        ],
    },
    {
        "name": "motivation",
        "keywords": [
            r"\bmotivat",                # "motivate", "motivated", "motivation", "motivating"
            r"\bno motivation\b",        # "I have no motivation"
            r"\bneed motivation\b",      # "I need motivation to study"
            r"\bstay motivated\b",       # "how can I stay motivated"
            r"\blazy\b",                 # "I'm feeling lazy"
            r"\bdon't feel like stud",   # "I don't feel like studying"
            r"\bnot in the mood.*stud",  # "I'm not in the mood to study"
            r"\bfeel like giving up\b",  # "I feel like giving up"
            r"\bgive up\b",
            r"\bconfidence\b",
            r"\bstress\b",
            r"\banxious\b",
            r"\bworried\b",
            r"\bcan'?t do\b",
            r"\btoo hard\b",
            r"\bstruggl",               # "struggle", "struggling"
        ],
        "responses": [
            (
                "Hey, don't be too hard on yourself! 💜\n\n"
                "You don't have to finish everything at once. Start with one small task and "
                "study for just 10 minutes — once you begin, it usually gets easier!\n\n"
                "Every small step counts! Here are some motivation boosters:\n"
                "  🎯  Set one tiny goal for today (e.g. 'read 2 pages')\n"
                "  🏆  Reward yourself after completing each goal\n"
                "  👫  Study with a friend for accountability\n"
                "  📊  Track your achievements — seeing progress keeps you going\n"
                "  📌  Remind yourself WHY you started studying\n\n"
                "Take a short break when you need one, and remember: you've got this! 🌟"
            ),
        ],
    },
    {
        "name": "sleep",
        "keywords": [
            r"\bsleep\b", r"\brest\b", r"\bbed\b", r"\btired\b",
            r"\binsomnia\b", r"\bstay up late\b", r"\ball.?night\b",
        ],
        "responses": [
            (
                "Sleep is a secret study weapon! 😴 Your brain consolidates memories while you sleep.\n\n"
                "  ✅  Aim for 8–10 hours of sleep each night\n"
                "  ✅  Avoid screens for at least 30 minutes before bed\n"
                "  ✅  Try to go to bed at the same time each night\n\n"
                "Pulling all-nighters actually makes your memory WORSE. Rest is part of studying! 🧠"
            ),
        ],
    },
    {
        "name": "homework_refusal",
        "keywords": [
            r"\bdo my homework\b", r"\bwrite my essay\b",
            r"\bcomplete.*assignment\b", r"\bsolve.*exam\b",
            r"\banswer.*question.*me\b", r"\bdo.*test\b",
        ],
        "responses": [
            (
                "I'm afraid I can't do that for you. 🚫\n\n"
                "My role is to help you *learn how* to study, not to do the work for you.\n"
                "Here's what I CAN do:\n"
                "  ✅  Give you study strategies and tips\n"
                "  ✅  Help you create a study plan\n"
                "  ✅  Teach you memory and revision techniques\n\n"
                "What study skill would you like to work on? 📚"
            ),
        ],
    },
    {
        "name": "help",
        "keywords": [
            r"\bhelp\b", r"\bwhat can you do\b", r"\bwhat do you do\b",
            r"\boptions\b", r"\bmenu\b", r"\btopic\b",
        ],
        "responses": [
            (
                "Here's what I can help you with! 📋\n\n"
                "  📚  Study tips & habits\n"
                "  🧠  Memory techniques\n"
                "  ⏱️  Study breaks & Pomodoro\n"
                "  📵  Avoiding distractions\n"
                "  📅  Making a study plan or timetable\n"
                "  ✏️  Note-taking methods\n"
                "  📖  Revision strategies\n"
                "  💪  Motivation & dealing with stress\n"
                "  😴  Sleep & rest advice\n\n"
                "Just type anything related to studying and I'll guide you! 😊"
            ),
        ],
    },
    {
        "name": "goodbye",
        "keywords": [
            r"\bbye\b", r"\bgoodbye\b", r"\bsee you\b",
            r"\bthanks\b", r"\bthank you\b", r"\bthx\b",
            r"\bcheers\b",
        ],
        "responses": [
            "You're welcome! Good luck with your studies! 🌟 Come back any time you need help.",
            "Bye! Keep studying smart, not just hard. 💡 You've got this! 👋",
            "Thanks for chatting! Remember: small daily improvements lead to big results. 📈 See you soon! 😊",
        ],
    },
]

FALLBACK_RESPONSES = [
    (
        "Hmm, I'm not sure I understand that. 🤔 I'm designed to help with study tips!\n\n"
        "Try asking me about:\n"
        "  📚  Study habits\n  🧠  Memory techniques\n  📅  Study planning\n  ⏱️  Taking breaks\n\n"
        "Or just type *help* to see everything I can do!"
    ),
    (
        "I didn't quite catch that. 😅 I'm a study-focused bot, so let's keep things academic!\n"
        "Type *help* to see what I can assist you with."
    ),
]


def get_response(user_input: str) -> str:
    """
    Match user_input against intents and return an appropriate response.
    Falls back to FALLBACK_RESPONSES if no intent matched.
    """
    text = user_input.lower().strip()

    for intent in INTENTS:
        for pattern in intent["keywords"]:
            if re.search(pattern, text):
                return random.choice(intent["responses"])

    return random.choice(FALLBACK_RESPONSES)


# ── Self-test ────────────────────────────────────────────────────────────────
def _intent_name(user_input: str) -> Optional[str]:
    """Return the matched intent name (or None for fallback)."""
    text = user_input.lower().strip()
    for intent in INTENTS:
        for pattern in intent["keywords"]:
            if re.search(pattern, text):
                return intent["name"]
    return None


def run_tests() -> None:
    """
    Assert that all required example inputs map to their expected intents,
    then print a full demo of extra inputs.
    """
    required = [
        # ── Previous 8 (from last session) ──────────────────────────────────
        ("give me some study tips",                              "general_study_tips"),
        ("What are some effective study techniques?",            "general_study_tips"),
        ("How can I study better?",                              "improve_study_habits"),
        ("How can I improve my study habits?",                   "improve_study_habits"),
        ("How can I remember what I learn?",                     "memory_techniques"),
        ("How can I improve my memory?",                         "memory_techniques"),
        ("Should I take breaks while studying?",                 "breaks"),
        ("How can I avoid distractions when studying?",          "distractions"),
        ("Can you help me make a study timetable?",              "study_plan"),
        ("How can I take better notes?",                         "notes"),
        ("How should I prepare for my exams?",                   "revision"),
        # ── Motivation examples ──────────────────────────────────────────────
        ("I need motivation to study.",                          "motivation"),
        ("I don't feel like studying.",                          "motivation"),
        ("I'm feeling lazy today.",                              "motivation"),
        ("How can I stay motivated to study?",                   "motivation"),
        ("I feel like giving up on my studies.",                 "motivation"),
        ("Motivation",                                           "motivation"),
    ]

    print("=" * 60)
    print("REQUIRED INTENT TESTS")
    print("=" * 60)
    all_passed = True
    for text, expected in required:
        got = _intent_name(text)
        status = "PASS ✅" if got == expected else f"FAIL ❌  (got: {got!r})"
        if got != expected:
            all_passed = False
        print(f"[{status}]")
        print(f"  Input    : {text}")
        print(f"  Expected : {expected}")
        print("-" * 60)

    print()
    if all_passed:
        print("All required tests PASSED. ✅")
    else:
        print("Some tests FAILED. ❌  See details above.")

    # ── Additional smoke-test inputs (no assertions, just show responses) ────
    extras = [
        "Hi there!",
        "Should I take a break?",
        "How do I avoid distractions?",
        "Can you help me make a study plan?",
        "I need a timetable template",
        "How should I take notes?",
        "How do I revise for exams?",
        "I feel like giving up",
        "Do my homework for me",
        "What can you do?",
        "Thanks, bye!",
        "improve my studying",
        "help me study",
        "I'm not in the mood to study",
        "I have no motivation today",
        "What is the capital of France?",  # off-topic — should fallback
    ]
    print()
    print("=" * 60)
    print("EXTRA SMOKE TESTS  (responses only, no assertions)")
    print("=" * 60)
    for inp in extras:
        print(f"User : {inp}")
        print(f"Bot  : {get_response(inp)[:80]}…")
        print("-" * 60)


if __name__ == "__main__":
    run_tests()
