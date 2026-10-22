"""
Study Buddy Bot — Telegram Integration
Uses python-telegram-bot v20+ (async).
Imports the rule-based engine from bot_engine.py.

Setup:
  1. pip install python-telegram-bot
  2. Set your token in the BOT_TOKEN variable below (or via environment variable).
  3. python telegram_bot.py
"""

import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Import the shared rule-based engine
from bot_engine import get_response

# ── Configuration ────────────────────────────────────────────────────────────
# Replace the empty string with your BotFather token,
# OR set the environment variable TELEGRAM_BOT_TOKEN before running.
BOT_TOKEN: str = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_BOTFATHER_TOKEN_HERE")

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ── Keyboard quick-reply labels (shown as custom keyboard) ────────────────────
QUICK_REPLIES = [
    ["📚 Study tips", "🧠 Memory techniques"],
    ["⏱️ Study breaks", "📵 Avoid distractions"],
    ["📅 Study plan", "✏️ Note-taking tips"],
    ["📖 Revision strategies", "💪 Motivation"],
    ["❓ Help"],
]


def _make_keyboard():
    """Return a ReplyKeyboardMarkup for quick replies."""
    from telegram import ReplyKeyboardMarkup

    return ReplyKeyboardMarkup(
        QUICK_REPLIES,
        resize_keyboard=True,
        input_field_placeholder="Ask me anything about studying…",
    )


# ── Handlers ──────────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the user sends /start."""
    welcome = (
        "Hey! 👋 I'm *Study Buddy Bot* — your friendly academic support bot!\n\n"
        "I can help you with:\n"
        "  📚  Study tips & habits\n"
        "  🧠  Memory techniques\n"
        "  ⏱️  Study breaks (Pomodoro)\n"
        "  📵  Avoiding distractions\n"
        "  📅  Making a study plan\n"
        "  ✏️  Note-taking methods\n"
        "  📖  Revision strategies\n"
        "  💪  Motivation & stress tips\n\n"
        "Use the buttons below or just type your question! 😊"
    )
    await update.message.reply_text(
        welcome,
        parse_mode="Markdown",
        reply_markup=_make_keyboard(),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Respond to /help."""
    await update.message.reply_text(
        get_response("help"),
        reply_markup=_make_keyboard(),
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process any text message through the rule-based engine."""
    user_text = update.message.text
    logger.info("User [%s]: %s", update.effective_user.first_name, user_text)

    # Strip emoji/button prefixes so patterns still match
    clean_text = user_text.lstrip("📚🧠⏱️📵📅✏️📖💪❓ ")

    response = get_response(clean_text)
    await update.message.reply_text(response, reply_markup=_make_keyboard())


# ── Entry point ───────────────────────────────────────────────────────────────
def main() -> None:
    if BOT_TOKEN == "YOUR_BOTFATHER_TOKEN_HERE":
        logger.error(
            "Please set your Telegram bot token!\n"
            "  Option 1 — Environment variable:  set TELEGRAM_BOT_TOKEN=<your-token>\n"
            "  Option 2 — Edit BOT_TOKEN in telegram_bot.py"
        )
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Study Buddy Bot is running… Press Ctrl-C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
