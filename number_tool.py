from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import ContextTypes
import os

# স্টাইল ইম্পোর্ট এবং এরর হ্যান্ডলিং (টার্মাক্স বা পুরনো ভার্সনের এরর ফিক্স)
try:
    from telegram.constants import KeyboardButtonStyle
    STYLE_BLUE = getattr(KeyboardButtonStyle, 'PRIMARY', None)
    STYLE_RED = getattr(KeyboardButtonStyle, 'DESTRUCTIVE', None)
except ImportError:
    STYLE_BLUE = None
    STYLE_RED = None

# ✅ কাস্টম কালারফুল কিবোর্ড ফাংশন
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
                # বাকি সব বাটন নীল (Blue) হবে
                styled_row.append(KeyboardButton(text, style=STYLE_BLUE))
        styled_rows.append(styled_row)
    return ReplyKeyboardMarkup(styled_rows, resize_keyboard=True)

# ===== MENU =====
NUMBER_MENU = [
    ["➕ FORMAT NUMBERS"],
    ["🔙 BACK"]
]

async def number_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # ===== BACK =====
    if text == "🔙 BACK":
        context.user_data.clear()
        # মেইন মেনু বাটনগুলো (উদাহরণস্বরূপ এখানে দেওয়া হলো)
        main_btns = [
            ["📱 NUMBERS"],
            ["📲 OTP MANAGER", "📧 EMAIL TOOL"],
            ["📞 NUMBER TOOL", "🔁 REPEAT TOOL"],
            ["🔍 SEARCH COUNTRY"],
            ["ℹ️ HELP"]
        ]
        return await update.message.reply_text(
            '<tg-emoji emoji-id="5260433458324322750">🔙</tg-emoji> <b>Back to Main Menu</b>',
            parse_mode="HTML",
            reply_markup=get_blue_keyboard(main_btns)
        )

    # ===== MENU =====
    if text == "📞 NUMBER TOOL":
        msg = (
            "<b>╔══════════════════════╗</b>\n"
            "<b> <tg-emoji emoji-id=\"5467539229468793355\">📞</tg-emoji> NUMBER TOOL </b>\n"
            "<b>╚══════════════════════╝</b>\n\n"

            '<tg-emoji emoji-id="6232999738459823976">✅</tg-emoji> <b>Status:</b> Ready\n'
            '<tg-emoji emoji-id="5345905193005371012">⚡️</tg-emoji> <b>Speed:</b> Fast\n\n'

            '<tg-emoji emoji-id="5296369303661067030">📤</tg-emoji> <i>Send numbers to format</i>'
        )

        return await update.message.reply_text(
            msg,
            parse_mode="HTML",
            reply_markup=get_blue_keyboard(NUMBER_MENU)
        )

    # ===== START =====
    if text == "➕ FORMAT NUMBERS":
        context.user_data["step"] = "format"
        return await update.message.reply_text(
            '<tg-emoji emoji-id="5345905193005371012">⚡️</tg-emoji> <b>Send numbers line by line</b>',
            parse_mode="HTML",
            reply_markup=get_blue_keyboard([["🔙 BACK"]]) # এখানে ব্যাক বাটনটি লাল হবে
        )

    # ===== PROCESS =====
    if context.user_data.get("step") == "format":
        lines = text.split("\n")
        out = []

        for n in lines:
            n = n.strip()
            if not n: continue
            
            # সংখ্যা থেকে অপ্রয়োজনীয় চিহ্ন সরানো কিন্তু ফরম্যাট রাখা
            clean_n = "".join(filter(str.isdigit, n))
            
            if not clean_n:
                continue

            if not n.startswith("+"):
                n = "+" + clean_n
            else:
                n = "+" + clean_n

            out.append(n)

        if not out:
            return await update.message.reply_text(
                '<tg-emoji emoji-id="6230838059944909526">❌</tg-emoji> <b>No valid numbers</b>',
                parse_mode="HTML",
                reply_markup=get_blue_keyboard([["🔙 BACK"]])
            )

        # ===== FILE =====
        file_name = "formatted_numbers.txt"

        with open(file_name, "w") as f:
            f.write("\n".join(out))

        # 💎 PREMIUM MESSAGE
        await update.message.reply_text(
            "<b>╔══════════════════════╗</b>\n"
           "<b>   <tg-emoji emoji-id=\"5467539229468793355\">📞</tg-emoji> FORMAT COMPLETE DONE <tg-emoji emoji-id=\"6233111716847165087\">👨‍💻</tg-emoji>   </b>\n" 
            "<b>╚══════════════════════╝</b>\n\n"
            f'<tg-emoji emoji-id="6232999738459823976">✅</tg-emoji> <b>Total:</b> <code>{len(out)}</code>\n'
            '<tg-emoji emoji-id="5345905193005371012">⚡️</tg-emoji> <i>File ready below</i>',
            parse_mode="HTML",
            reply_markup=get_blue_keyboard(NUMBER_MENU)
        )

        # 📤 SEND FILE
        await update.message.reply_document(open(file_name, "rb"))

        os.remove(file_name)
        context.user_data.clear()
