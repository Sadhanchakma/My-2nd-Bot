import os
from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import ContextTypes

# স্টাইল ইম্পোর্ট এবং এরর হ্যান্ডলিং (টার্মাক্স বা পুরনো ভার্সনের জন্য)
try:
    from telegram.constants import KeyboardButtonStyle
    STYLE_BLUE = getattr(KeyboardButtonStyle, 'PRIMARY', None)
    STYLE_RED = getattr(KeyboardButtonStyle, 'DESTRUCTIVE', None)
except ImportError:
    STYLE_BLUE = None
    STYLE_RED = None

# ✅ কালারফুল কিবোর্ড ফাংশন
def get_blue_keyboard(buttons):
    if STYLE_BLUE is None:
        return ReplyKeyboardMarkup([[KeyboardButton(text) for text in row] for row in buttons], resize_keyboard=True)

    styled_rows = []
    for row in buttons:
        styled_row = []
        for text in row:
            # BACK বাটন লাল (Red) হবে
            if text in ["🔙 BACK", "BACK", "❌ Cancel"]:
                style = STYLE_RED if STYLE_RED else STYLE_BLUE
                styled_row.append(KeyboardButton(text, style=style))
            else:
                # বাকি সব নীল (Blue) হবে
                styled_row.append(KeyboardButton(text, style=STYLE_BLUE))
        styled_rows.append(styled_row)
    return ReplyKeyboardMarkup(styled_rows, resize_keyboard=True)

# ===== MENU =====
REPEAT_MENU = [
    ["▶️ START REPEAT"],
    ["🔙 BACK"]
]

async def repeat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text if update.message.text else ""

    # ===== BACK =====
    if text == "🔙 BACK":
        context.user_data.clear()
        main_btns = [["📱 NUMBERS"],["📲 OTP MANAGER", "📧 EMAIL TOOL"], ["📞 NUMBER TOOL", "🔁 REPEAT TOOL"], ["ℹ️ HELP"]]
        return await update.message.reply_text(
            '<tg-emoji emoji-id="5260433458324322750">🔙</tg-emoji> <b>Back to Main Menu</b>',
            parse_mode="HTML",
            reply_markup=get_blue_keyboard(main_btns)
        )

    # ===== MENU =====
    if text == "🔁 REPEAT TOOL":
        msg = (
            "<b>╔══════════════════════╗</b>\n"
            "<b> <tg-emoji emoji-id=\"5334565920998175923\">🔁</tg-emoji> REPEAT TOOL </b>\n"
            "<b>╚══════════════════════╝</b>\n\n"

            '<tg-emoji emoji-id="6232999738459823976">✅</tg-emoji> Ready\n'
            '<tg-emoji emoji-id="5345905193005371012">⚡️</tg-emoji> Repeat Mode\n\n'

            '<tg-emoji emoji-id="5296369303661067030">📤</tg-emoji> Click start'
        )

        return await update.message.reply_text(
            msg,
            parse_mode="HTML",
            reply_markup=get_blue_keyboard(REPEAT_MENU)
        )

    # ===== START =====
    if text == "▶️ START REPEAT":
        context.user_data["step"] = "text"

        msg = (
            "<b>╔══════════════════════╗</b>\n"
            "<b> <tg-emoji emoji-id=\"5334565920998175923\">🔁</tg-emoji> START REPEAT </b>\n"
            "<b>╚══════════════════════╝</b>\n\n"

            '<tg-emoji emoji-id="5345905193005371012">⚡️</tg-emoji> <b>Send your text</b>'
        )

        return await update.message.reply_text(
            msg, 
            parse_mode="HTML",
            reply_markup=get_blue_keyboard([["🔙 BACK"]])
        )

    # ===== TEXT =====
    if context.user_data.get("step") == "text":
        context.user_data["txt"] = text
        context.user_data["step"] = "count"

        msg = (
            "<b>╔══════════════════════╗</b>\n"
            "<b> <tg-emoji emoji-id=\"6230809013081086802\">📌</tg-emoji> SET COUNT </b>\n"
            "<b>╚══════════════════════╝</b>\n\n"

            '<tg-emoji emoji-id="6232999738459823976">✅</tg-emoji> Text saved\n'
            '<tg-emoji emoji-id="5345905193005371012">⚡️</tg-emoji> Enter repeat count'
        )

        return await update.message.reply_text(
            msg, 
            parse_mode="HTML",
            reply_markup=get_blue_keyboard([["🔙 BACK"]])
        )

    # ===== COUNT =====
    if context.user_data.get("step") == "count":
        try:
            c = int(text)

            if c <= 0:
                return await update.message.reply_text(
                    '<tg-emoji emoji-id="6230838059944909526">❌</tg-emoji> Invalid count',
                    parse_mode="HTML",
                    reply_markup=get_blue_keyboard([["🔙 BACK"]])
                )

            # সীমা নির্ধারণ (বট ক্র্যাশ রোধে ১০ হাজার পর্যন্ত রাখা ভালো)
            if c > 10000:
                return await update.message.reply_text(
                    '❌ <b>Max limit 10,000</b>', 
                    parse_mode="HTML",
                    reply_markup=get_blue_keyboard([["🔙 BACK"]])
                )

            result = "\n".join([context.user_data["txt"]] * c)

            file_name = "repeat_result.txt"
            with open(file_name, "w") as f:
                f.write(result)

            # 💎 PREMIUM MSG
            await update.message.reply_text(
                "<b>╔══════════════════════╗</b>\n"
                "<b> <tg-emoji emoji-id=\"5334565920998175923\">🔁</tg-emoji> REPEAT COMPLETE </b>\n"
                "<b>╚══════════════════════╝</b>\n\n"
                f'<tg-emoji emoji-id="6232999738459823976">✅</tg-emoji> <b>Total:</b> <code>{c}</code>\n'
                '<tg-emoji emoji-id="5345905193005371012">⚡️</tg-emoji> <i>File ready below</i>',
                parse_mode="HTML",
                reply_markup=get_blue_keyboard(REPEAT_MENU)
            )

            await update.message.reply_document(open(file_name, "rb"))

            os.remove(file_name)
            context.user_data.clear()

        except ValueError:
            return await update.message.reply_text(
                '<tg-emoji emoji-id="6230838059944909526">❌</tg-emoji> Enter valid number',
                parse_mode="HTML",
                reply_markup=get_blue_keyboard([["🔙 BACK"]])
            )
