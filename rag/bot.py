from pydantic_settings import BaseSettings
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
)
from telegram.ext import filters
from .chat import chat


class BotSubcommand(BaseSettings):
    api_key: str

    def cli_cmd(self) -> None:
        run_bot(self.api_key)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!",
    )


async def do_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_reply = await chat(update.message.text)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=chat_reply,
    )


def run_bot(api_key: str):
    application = ApplicationBuilder().token(api_key).build()

    start_handler = CommandHandler("start", start)
    chat_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), do_chat)
    application.add_handler(start_handler)
    application.add_handler(chat_handler)

    application.run_polling()
