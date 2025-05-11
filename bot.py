import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from config import TELEGRAM_TOKEN, DEFAULT_AI
from memory import load_memory, save_memory
from ai_engines.gpt_engine import chat_with_gpt
from ai_engines.gemini_engine import chat_with_gemini

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def select_engine():
    if DEFAULT_AI == "gpt":
        return chat_with_gpt
    elif DEFAULT_AI == "gemini":
        return chat_with_gemini
    else:
        return chat_with_gpt

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحبًا بك في MeDo Chat AI Pro!\n"
        "استخدم الأوامر التالية:\n"
        "/code [سؤالك] - للبرمجة\n"
        "/advice [سؤالك] - للنصائح\n"
        "/translate [النص] - للترجمة\n"
        "/summarize [النص] - للتلخيص\n"
        "أو أرسل رسالة عادية للتحدث معي."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_message = update.message.text

    messages = load_memory(user_id)

    if user_message.startswith("/code "):
        role = "أنت مساعد برمجة محترف. جاوب بشكل عملي وواضح بكود إن أمكن."
        prompt = user_message[6:]
    elif user_message.startswith("/advice "):
        role = "أنت خبير نصائح ذكي. جاوب بحكمة ونضج."
        prompt = user_message[8:]
    elif user_message.startswith("/translate "):
        role = "ترجم النص التالي للإنجليزية أو العربية حسب اللغة."
        prompt = user_message[11:]
    elif user_message.startswith("/summarize "):
        role = "لخص النص التالي بشكل احترافي وواضح."
        prompt = user_message[11:]
    else:
        role = "أنت مساعد ذكي اسمه MeDo Chat AI. جاوب على أي نوع من الأسئلة."
        prompt = user_message

    messages.append({"role": "system", "content": role})
    messages.append({"role": "user", "content": prompt})

    engine = select_engine()

    try:
        reply = engine(messages)
        messages.append({"role": "assistant", "content": reply})
        save_memory(user_id, messages)
        await update.message.reply_text(reply)
    except Exception as e:
        logger.error(e)
        await update.message.reply_text("حدث خطأ أثناء المعالجة. الرجاء المحاولة مرة أخرى لاحقًا.")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()