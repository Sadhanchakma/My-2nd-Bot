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
            # BACK বা CLEAR বাটন লাল (Red) হবে
            if text in ["🔙 BACK", "BACK", "🗑️ CLEAR", "❌ Cancel"]:
                style = STYLE_RED if STYLE_RED else STYLE_BLUE
                styled_row.append(KeyboardButton(text, style=style))
            else:
                # বাকি সব নীল (Blue) হবে
                styled_row.append(KeyboardButton(text, style=STYLE_BLUE))
        styled_rows.append(styled_row)
    return ReplyKeyboardMarkup(styled_rows, resize_keyboard=True)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def user_file(uid): return f"{DATA_DIR}/{uid}.txt"
def used_file(uid): return f"{DATA_DIR}/{uid}_used.txt"

# ================= PARSE =================
def parse_line(line):
    parts = line.split("|")
    if len(parts) < 2:
        return None, None
    return parts[0].strip(), parts[-1].strip()

# ================= GET NEXT =================
def get_next(uid):
    path = user_file(uid)
    used = used_file(uid)

    if not os.path.exists(path): return None

    with open(path) as f:
        lines = f.readlines()

    if not lines: return None

    line = lines[0].strip()

    with open(path, "w") as f:
        f.writelines(lines[1:])

    with open(used, "a") as f:
        f.write(line + "\n")

    num, otp = parse_line(line)
    return num, otp, len(lines)

# ================= MENU =================
OTP_MENU = [
    ["⚡ GET OTP", "🔄 NEXT OTP"],
    ["📊 MY STATS", "📤 UPLOAD"],
    ["🗑️ CLEAR", "🔙 BACK"]
]

# ================= HANDLER =================
async def otp_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text if update.message.text else ""

    # ===== FILE UPLOAD =====
    if update.message.document and context.user_data.get("upload_mode"):
        doc = update.message.document

        if not doc.file_name.endswith(".txt"):
            return await update.message.reply_text(
                '<tg-emoji emoji-id="6230838059944909526">❌</tg-emoji> <b>Invalid file format</b>\n'
                '<i>Only .txt files allowed</i>',
                parse_mode="HTML",
                reply_markup=get_blue_keyboard([["🔙 BACK"]])
            )

        file = await doc.get_file()
        temp = f"{uid}.txt"
        await file.download_to_drive(temp)

        with open(temp) as f:
            new_lines = f.readlines()

        with open(user_file(uid), "a") as f:
            f.writelines(new_lines)

        os.remove(temp)
        context.user_data["upload_mode"] = False

        return await update.message.reply_text(
            "<b>╔══════════════════════╗</b>\n"
            "<b> <tg-emoji emoji-id=\"6232999738459823976\">✅</tg-emoji> UPLOAD SUCCESS </b>\n"
            "<b>╚══════════════════════╝</b>\n\n"

            f'<tg-emoji emoji-id="6233241506463883080">📊</tg-emoji> <b>Total Added:</b> <code>{len(new_lines)}</code>\n'
            '<tg-emoji emoji-id="5345905193005371012">⚡️</tg-emoji> <i>System Ready</i>',
            parse_mode="HTML",
            reply_markup=get_blue_keyboard(OTP_MENU)
        )

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
    if text == "📲 OTP MANAGER":
        return await update.message.reply_text(
            "<b>╔══════════════════════╗</b>\n"
            "<b> <tg-emoji emoji-id=\"5406809207947142040\">📲</tg-emoji> OTP MANAGER </b>\n"
            "<b>╚══════════════════════╝</b>\n\n"

            '<tg-emoji emoji-id="6232999738459823976">✅</tg-emoji> <b>Status:</b> Active\n'
            '<tg-emoji emoji-id="5345905193005371012">⚡️</tg-emoji> <b>Mode:</b> OTP System\n\n'

            '<tg-emoji emoji-id="5296369303661067030">📤</tg-emoji> <i>Select option below</i>',
            parse_mode="HTML",
            reply_markup=get_blue_keyboard(OTP_MENU)
        )

    # ===== UPLOAD BUTTON =====
    if text == "📤 UPLOAD":
        context.user_data["upload_mode"] = True
        return await update.message.reply_text(
            "<b>╔══════════════════════╗</b>\n"
            "<b> <tg-emoji emoji-id=\"5296369303661067030\">📤</tg-emoji> UPLOAD MODE </b>\n"
            "<b>╚══════════════════════╝</b>\n\n"

            '<tg-emoji emoji-id="5345905193005371012">⚡️</tg-emoji> <b>Status:</b> Waiting\n'
            '<tg-emoji emoji-id="5433614747381538714">📌</tg-emoji> <i>Uplode your .txt file now</i>',
            parse_mode="HTML",
            reply_markup=get_blue_keyboard([["🔙 BACK"]])
        )

    # ===== GET OTP / NEXT OTP =====
    if text in ["⚡ GET OTP", "🔄 NEXT OTP"]:
        data = get_next(uid)
        if not data:
            return await update.message.reply_text(
                '<tg-emoji emoji-id="6230838059944909526">❌</tg-emoji> <b>No OTP available</b>',
                parse_mode="HTML",
                reply_markup=get_blue_keyboard(OTP_MENU)
            )

        num, otp, left = data

        return await update.message.reply_text(
            "<b>╔══════════════════════╗</b>\n"
            "<b> <tg-emoji emoji-id=\"6233241506463883080\">📊</tg-emoji> OTP RESULT </b>\n"
            "<b>╚══════════════════════╝</b>\n\n"

            f"<code>{num} | {otp}</code>\n\n"

            f'<tg-emoji emoji-id="6233241506463883080">📊</tg-emoji> <b>Left:</b> <code>{left-1}</code>',
            parse_mode="HTML",
            reply_markup=get_blue_keyboard(OTP_MENU)
        )

    # ===== STATS =====
    if text == "📊 MY STATS":
        count = 0
        if os.path.exists(user_file(uid)):
            with open(user_file(uid)) as f:
                count = len(f.readlines())

        return await update.message.reply_text(
            "<b>╔══════════════════════╗</b>\n"
            "<b> <tg-emoji emoji-id=\"6233241506463883080\">📊</tg-emoji> MY STATS </b>\n"
            "<b>╚══════════════════════╝</b>\n\n"

            f'<tg-emoji emoji-id="6233241506463883080">📊</tg-emoji> <b>Remaining OTP:</b> <code>{count}</code>',
            parse_mode="HTML",
            reply_markup=get_blue_keyboard(OTP_MENU)
        )

    # ===== CLEAR =====
    if text == "🗑️ CLEAR":
        if os.path.exists(user_file(uid)): os.remove(user_file(uid))
        if os.path.exists(used_file(uid)): os.remove(used_file(uid))

        return await update.message.reply_text(
            "<b>╔══════════════════════╗</b>\n"
            "<b> <tg-emoji emoji-id=\"6230838059944909526\">❌</tg-emoji> DATA CLEARED </b>\n"
            "<b>╚══════════════════════╝</b>\n\n"

            '<tg-emoji emoji-id="6230838059944909526">❌</tg-emoji> <b>All OTP removed</b>',
            parse_mode="HTML",
            reply_markup=get_blue_keyboard(OTP_MENU)
        )

    # ===== SEARCH (Default fallback if not a button text) =====
    found = False
    for fpath in [user_file(uid), used_file(uid)]:
        if not os.path.exists(fpath): continue

        with open(fpath) as f:
            for line in f:
                num, otp = parse_line(line)
                if num and text in num:
                    await update.message.reply_text(
                        "<b>╔══════════════════════╗</b>\n"
                        "<b> 🔍 SEARCH RESULT </b>\n"
                        "<b>╚══════════════════════╝</b>\n\n"
                        f"<code>{num} | {otp}</code>",
                        parse_mode="HTML",
                        reply_markup=get_blue_keyboard(OTP_MENU)
                    )
                    found = True
                    break
        if found: break

    if not found and text:
        return await update.message.reply_text(
            '<tg-emoji emoji-id="6230838059944909526">❌</tg-emoji> <b>Not found or invalid command</b>',
            parse_mode="HTML",
            reply_markup=get_blue_keyboard(OTP_MENU)
        )
