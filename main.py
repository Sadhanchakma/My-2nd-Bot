from telegram import ReplyKeyboardMarkup, Update, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# আপনার আগের ইমপোর্টগুলো
from otp_manager import otp_handler
from email_tool import email_handler
from number_tool import number_handler
from repeat_tool import repeat_handler
try:
    from job_number_tool import job_number_handler
except ImportError:
    job_number_handler = None

# ✅ TOKEN
TOKEN = "8658364991:AAEYny80WCZh3lgf0JMFpYhcxdiO0tE31so"

# ✅ 🔵 BULLETPROOF BLUE KEYBOARD SYSTEM
def get_blue_keyboard(buttons):
    """রেলওয়ে এবং সব হোস্টিংয়ে ব্লু বাটন নিশ্চিত করার জন্য আপডেট করা ফাংশন"""
    try:
        # লেটেস্ট ভার্সনে ব্লু স্টাইল ইমপোর্ট করা
        from telegram.constants import KeyboardButtonStyle
        PRIMARY_STYLE = KeyboardButtonStyle.PRIMARY
    except (ImportError, AttributeError):
        # যদি লাইব্রেরি পুরনো হয় তবে স্টাইল বাদ রাখা
        PRIMARY_STYLE = None

    blue_keyboard = []
    for row in buttons:
        if PRIMARY_STYLE:
            # স্টাইল থাকলে ব্লু বাটন তৈরি
            blue_row = [KeyboardButton(text=str(text), style=PRIMARY_STYLE) for text in row]
        else:
            # না থাকলে রেগুলার বাটন
            blue_row = [KeyboardButton(text=str(text)) for text in row]
        blue_keyboard.append(blue_row)
    
    return ReplyKeyboardMarkup(blue_keyboard, resize_keyboard=True)


# ===== MAIN MENU =====
MAIN_MENU = [
    ["📱 NUMBERS"],
    ["📲 OTP MANAGER", "📧 EMAIL TOOL"],
    ["📞 NUMBER TOOL", "🔁 REPEAT TOOL"],
    ["ℹ️ HELP"]
]


# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    start_msg = (
        "<b>╔══════════════════════╗</b>\n"
        "<b>   <tg-emoji emoji-id=\"5332586662629227075\">👨‍💻</tg-emoji> ALL-IN-ONE BOT <tg-emoji emoji-id=\"5332586662629227075\">👨‍💻</tg-emoji>   </b>\n"
        "<b>╚══════════════════════╝</b>\n\n"
        '<tg-emoji emoji-id="5345905193005371012">⚡️</tg-emoji> <b>Status:</b> <code>Online & Ready</code>\n'
        '<tg-emoji emoji-id="6206505206197261313">📊</tg-emoji> <b>System:</b> <code>High Performance</code>\n'
        '<tg-emoji emoji-id="6232999738459823976">✅</tg-emoji> <b>Access:</b> <code>Full Features Enabled</code>\n'
        "━━━━━━━━━━━━━━━━━━━━━\n"
        '<tg-emoji emoji-id="5296369303661067030">📤</tg-emoji> <i>নিচের মেনু থেকে আপনার প্রয়োজনীয় অপশনটি বেছে নিন</i>'
    )

    await update.message.reply_text(
        start_msg,
        parse_mode="HTML",
        reply_markup=get_blue_keyboard(MAIN_MENU) 
    )


# ================= ROUTER =================
async def router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        mode = context.user_data.get("mode")
        if mode == "job_number" and job_number_handler:
            return await job_number_handler(update, context)
        return

    text = update.message.text if update.message and update.message.text else None

    # ===== HELP =====
    if text == "ℹ️ HELP":
        help_text = (
            "<b>╔══ <tg-emoji emoji-id=\"5332679880599418983\">ℹ️</tg-emoji> HELP PANEL ══╗</b>\n\n"
            '<tg-emoji emoji-id="6213065824576478666">👨‍💻</tg-emoji> <b>Admin & Links</b>\n\n'
            "<i>Click buttons below</i>"
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👨‍💻 Admin", url="https://t.me/Sadhan_Chakma")],
            [InlineKeyboardButton("📢 Main Channel", url="https://t.me/Team_X_Run")],
            [InlineKeyboardButton("📦 APK Zone", url="https://t.me/+EflYyh6CP_AzZDBl")]
        ])
        return await update.message.reply_text(help_text, parse_mode="HTML", reply_markup=keyboard)

    # ===== BACK =====
    if text == "🔙 BACK":
        return await start(update, context)

    # ===== MAIN MENU ROUTING =====
    if text == "📲 OTP MANAGER":
        context.user_data["mode"] = "otp"
        return await otp_handler(update, context)

    if text == "📧 EMAIL TOOL":
        context.user_data["mode"] = "email"
        return await email_handler(update, context)

    if text == "📞 NUMBER TOOL":
        context.user_data["mode"] = "number"
        return await number_handler(update, context)

    if text == "🔁 REPEAT TOOL":
        context.user_data["mode"] = "repeat"
        return await repeat_handler(update, context)

    if text == "📱 NUMBERS":
        context.user_data["mode"] = "job_number"
        if job_number_handler:
            return await job_number_handler(update, context)
        else:
            return await update.message.reply_text("❌ Job Tool missing!")

    # ===== FILE HANDLING =====
    if update.message and update.message.document:
        mode = context.user_data.get("mode")
        if mode == "job_number" and job_number_handler:
            return await job_number_handler(update, context)
        else:
            return await otp_handler(update, context)

    # ===== MODE CALLBACKS =====
    mode = context.user_data.get("mode")

    if mode == "otp":
        await otp_handler(update, context)
    elif mode == "email":
        await email_handler(update, context)
    elif mode == "number":
        await number_handler(update, context)
    elif mode == "repeat":
        await repeat_handler(update, context)
    elif mode == "job_number" and job_number_handler:
        await job_number_handler(update, context)
    else:
        if update.message and not update.message.document:
            await update.message.reply_text(
                "❌ Unknown option or Invalid action",
                reply_markup=get_blue_keyboard([["🔙 BACK"]]) 
            )


# ================= RUN =================
def main():
    app = ApplicationBuilder().token(TOKEN).build() 

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(router))
    app.add_handler(MessageHandler(filters.ALL, router))

    print("Bot Running...")
    app.run_polling()


if __name__ == "__main__":
    main()
