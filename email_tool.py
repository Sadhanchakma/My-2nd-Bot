import random, os
from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import ContextTypes

# স্টাইল ইম্পোর্ট এবং এরর হ্যান্ডলিং (আপনার এরর ফিক্স করার জন্য)
try:
    from telegram.constants import KeyboardButtonStyle
    STYLE_BLUE = getattr(KeyboardButtonStyle, 'PRIMARY', None)
    STYLE_RED = getattr(KeyboardButtonStyle, 'DESTRUCTIVE', None)
except ImportError:
    STYLE_BLUE = None
    STYLE_RED = None

# ✅ কাস্টম ব্লু কিবোর্ড ফাংশন (আপনার কোনো ডিজাইন রিমুভ করবে না)
def get_blue_keyboard(buttons):
    if STYLE_BLUE is None:
        return ReplyKeyboardMarkup([[KeyboardButton(text) for text in row] for row in buttons], resize_keyboard=True)

    styled_rows = []
    for row in buttons:
        styled_row = []
        for text in row:
            if text in ["BACK", "🔙 Back", "❌ Cancel"]:
                # ব্যাক বাটন লাল করার চেষ্টা করবে
                style = STYLE_RED if STYLE_RED else STYLE_BLUE
                styled_row.append(KeyboardButton(text, style=style))
            else:
                # বাকি সব নীল
                styled_row.append(KeyboardButton(text, style=STYLE_BLUE))
        styled_rows.append(styled_row)
    return ReplyKeyboardMarkup(styled_rows, resize_keyboard=True)

# ===== MENU =====
EMAIL_MENU = [
    ["START EMAIL"],
    ["BACK"]
]

async def email_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # 🔥 BACK MUST BE FIRST
    if text == "BACK":
        context.user_data.clear()
        main_menu_btns = [
            ["📱 NUMBERS"],
            ["📲 OTP MANAGER", "📧 EMAIL TOOL"],
            ["📞 NUMBER TOOL", "🔁 REPEAT TOOL"],
            
            ["ℹ️ HELP"]
        ]
        return await update.message.reply_text(
            '<tg-emoji emoji-id="5260433458324322750">🔙</tg-emoji> <b>Back to main menu</b>',
            parse_mode="HTML",
            reply_markup=get_blue_keyboard(main_menu_btns)
        )

    # ===== MENU =====
    if text == "📧 EMAIL TOOL":
        menu_msg = (
            "<b>╔══════════════════════╗</b>\n"
            "<b>     <tg-emoji emoji-id=\"6165865413893689502\">👨‍💻</tg-emoji> EMAIL CONTROLLER <tg-emoji emoji-id=\"6165865413893689502\">👨‍💻</tg-emoji>     </b>\n"
            "<b>╚══════════════════════╝</b>\n\n"
            '<tg-emoji emoji-id="6231210205976206571">⚡️</tg-emoji> <b>Welcome to Premium Email Tool</b>\n'
            "━━━━━━━━━━━━━━━━━━━━━\n"
            '<tg-emoji emoji-id="5332679880599418983">ℹ️</tg-emoji> <b>Status:</b> <code>System Online</code> '
            '<tg-emoji emoji-id="6233111716847165087">✅</tg-emoji>\n'
            '<tg-emoji emoji-id="5345905193005371012">⚡️</tg-emoji> <b>Speed:</b> <code>High Speed</code> '
            '<tg-emoji emoji-id="6233144538987241810">➕</tg-emoji>\n'
            "━━━━━━━━━━━━━━━━━━━━━\n"
            '<tg-emoji emoji-id="5406745015365943482">📤</tg-emoji> <i>নিচের মেনু থেকে আপনার অপশনটি বেছে নিন:</i>'
        )

        return await update.message.reply_text(
            menu_msg,
            parse_mode="HTML",
            reply_markup=get_blue_keyboard(EMAIL_MENU)
        )

    # ===== START =====
    if text == "START EMAIL":
        context.user_data["step"] = "email"
        
        vip_message = (
            "<b>╔══════════════════════╗</b>\n"
            "<b>      <tg-emoji emoji-id=\"6213182012031769286\">✅</tg-emoji> আপনার জিমেইলটি পাঠাও <tg-emoji emoji-id=\"6213182012031769286\">✅</tg-emoji>      </b>\n"
            "<b>╚══════════════════════╝</b>\n\n"
            '<tg-emoji emoji-id="6231032948380935210">‼️</tg-emoji> <b>Status:</b> <code>Ready to Send</code>\n'
            '<tg-emoji emoji-id="5440411975509096877">📧</tg-emoji> <b>Action:</b> <i>Please provide the Gmail address</i>\n\n'
            "<b>━━━━━━━━━━━━━━━━━━━━━</b>\n"
            '<tg-emoji emoji-id="6084863769505171629">👨‍💻</tg-emoji> <i>নিচে আপনার জিমেইলটি টাইপ করে পাঠান...</i>'
        )

        return await update.message.reply_text(
            vip_message,
            parse_mode="HTML",
            reply_markup=get_blue_keyboard([["BACK"]])
        )

    # ===== EMAIL STEP =====
    if context.user_data.get("step") == "email":
        if "@" not in text:
            invalid_msg = (
                "<b>╔══════════════════════╗</b>\n"
                  "<b>      <tg-emoji emoji-id=\"6213182012031769286\">✅</tg-emoji> INVALID GMAIL <tg-emoji emoji-id=\"6213182012031769286\">✅</tg-emoji>      </b>\n"
                "<b>╚══════════════════════╝</b>\n\n"
                '<tg-emoji emoji-id="6230838059944909526">❌</tg-emoji> <b>Error:</b> <i>আপনার ইমেইলটি সঠিক নয়!</i>\n'
                '<tg-emoji emoji-id="5332679880599418983">ℹ️</tg-emoji> <b>Hint:</b> <code>example@gmail.com</code>'
            )
            return await update.message.reply_text(
                invalid_msg,
                parse_mode="HTML",
                reply_markup=get_blue_keyboard([["BACK"]])
            )

        context.user_data["email"] = text
        context.user_data["step"] = "count"

        success_msg = (
            "<b>╔══════════════════════╗</b>\n"
   "<b>      <tg-emoji emoji-id=\"6233111716847165087\">✅</tg-emoji> EMAIL VERIFIED <tg-emoji emoji-id=\"6233111716847165087\">✅</tg-emoji>      </b>\n"
    "<b>╚══════════════════════╝</b>\n\n"
       
            f'<tg-emoji emoji-id="5440411975509096877">📧</tg-emoji> <b>Target:</b> <code>{text}</code>\n'
            '<tg-emoji emoji-id="6231029967673630263">📊</tg-emoji> <b>Quantity:</b> <i>How many emails?</i>\n\n'
            '<tg-emoji emoji-id="5345905193005371012">⚡️</tg-emoji> <b>Limit:</b> <code>Max 10,000 only</code>\n'
            "<b>━━━━━━━━━━━━━━━━━━━━━</b>"
        )

        return await update.message.reply_text(
            success_msg,
            parse_mode="HTML",
            reply_markup=get_blue_keyboard([["BACK"]])
        )

    # ===== COUNT STEP =====
    if context.user_data.get("step") == "count":
        try:
            count = int(text.strip())

            # ❌ Invalid number
            if count <= 0:
                error_msg = (
                    "<b>╔══════════════════════╗</b>\n"
                    "<b>      <tg-emoji emoji-id=\"6230838059944909526\">❌</tg-emoji> INVALID NUMBER <tg-emoji emoji-id=\"6230838059944909526\">❌</tg-emoji>      </b>\n"
                    "<b>╚══════════════════════╝</b>\n\n"
                    '<tg-emoji emoji-id="6230838059944909526">❌</tg-emoji> <b>Error:</b> <i>আপনি সঠিক সংখ্যা দেননি!</i>\n'
                    '<tg-emoji emoji-id="5332679880599418983">ℹ️</tg-emoji> <b>Hint:</b> <code>1 - 10000</code> এর মধ্যে দিন\n\n'
                    '<tg-emoji emoji-id="5345905193005371012">⚡️</tg-emoji> <i>Try again...</i>'
                )
                return await update.message.reply_text(error_msg, parse_mode="HTML", reply_markup=get_blue_keyboard([["BACK"]]))

            # ❌ Limit exceeded
            if count > 10000:
                limit_msg = (
                    "<b>╔══════════════════════╗</b>\n"
                    "<b>      <tg-emoji emoji-id=\"6230838059944909526\">❌</tg-emoji> LIMIT EXCEEDED <tg-emoji emoji-id=\"6230838059944909526\">❌</tg-emoji>      </b>\n"
                    "<b>╚══════════════════════╝</b>\n\n"
                    '<tg-emoji emoji-id="5345905193005371012">⚡️</tg-emoji> <b>Maximum allowed:</b> <code>10,000</code>\n'
                    '<tg-emoji emoji-id="5332679880599418983">ℹ️</tg-emoji> <i>দয়া করে limit এর মধ্যে দিন</i>'
                )
                return await update.message.reply_text(limit_msg, parse_mode="HTML", reply_markup=get_blue_keyboard([["BACK"]]))

            email = context.user_data["email"]
            user, dom = email.split("@")
            file = f"{user}.txt"

            await update.message.reply_text(
                '<tg-emoji emoji-id="5345905193005371012">⚡️</tg-emoji> <b>Generating emails...</b>',
                parse_mode="HTML"
            )

            with open(file, "w") as f:
                for _ in range(count):
                    v1 = "".join(c.upper() if random.random()>0.5 else c.lower() for c in user)
                    v2 = "".join(c.upper() if random.random()>0.5 else c.lower() for c in dom)
                    f.write(f"{v1}@{v2}\n")

            await update.message.reply_document(open(file, "rb"))

            await update.message.reply_text(
                '<tg-emoji emoji-id="6232999738459823976">✅</tg-emoji> <b>File generated successfully!</b>\n'
                '<tg-emoji emoji-id="6206505206197261313">📊</tg-emoji> <i>Check your file above</i>',
                parse_mode="HTML",
                reply_markup=get_blue_keyboard(EMAIL_MENU)
            )

            os.remove(file)
            context.user_data.pop("step", None)

        except ValueError:
            return await update.message.reply_text(
                '<tg-emoji emoji-id="6230838059944909526">❌</tg-emoji> <b>শুধু number দাও</b>',
                parse_mode="HTML",
                reply_markup=get_blue_keyboard([["BACK"]])
            )
