import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

# স্টাইল ইম্পোর্ট এবং এরর হ্যান্ডলিং
try:
    from telegram.constants import KeyboardButtonStyle
    STYLE_BLUE = getattr(KeyboardButtonStyle, 'PRIMARY', None)
    STYLE_RED = getattr(KeyboardButtonStyle, 'DESTRUCTIVE', None)
except ImportError:
    STYLE_BLUE = None
    STYLE_RED = None

# ✅ কালারফুল কিবোর্ড ফাংশন
def get_job_keyboard(buttons):
    if STYLE_BLUE is None:
        return ReplyKeyboardMarkup([[KeyboardButton(text) for text in row] for row in buttons], resize_keyboard=True)

    styled_rows = []
    for row in buttons:
        styled_row = []
        for text in row:
            # BACK বা CLEAR বাটন লাল (Red) হবে
            if text in ["🔙 BACK", "BACK", "🗑 Clear All Stock", "❌ Clear All Stock", "❌ Cancel"]:
                style = STYLE_RED if STYLE_RED else STYLE_BLUE
                styled_row.append(KeyboardButton(text, style=style))
            else:
                styled_row.append(KeyboardButton(text, style=STYLE_BLUE))
        styled_rows.append(styled_row)
    return ReplyKeyboardMarkup(styled_rows, resize_keyboard=True)

# ফাইল লোকেশন
DB_FILE = "job_numbers.txt"
USED_FILE = "used_numbers.txt"

async def job_number_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    is_callback = False
    query = None
    if update.callback_query:
        is_callback = True
        query = update.callback_query
        await query.answer()
        text = query.data
    else:
        text = update.message.text if update.message and update.message.text else ""

        # ১. ফাইল আপলোড লজিক
    if update.message and update.message.document:
        doc = update.message.document
        if doc.file_name.endswith(".txt"):
            file = await doc.get_file()
            content = await file.download_as_bytearray()
            try:
                new_numbers = content.decode("utf-8").splitlines()
            except:
                new_numbers = content.decode("latin-1").splitlines()
            
            cleaned_numbers = [n.strip() for n in new_numbers if n.strip()]
            with open(DB_FILE, "a") as f:
                for num in cleaned_numbers:
                    f.write(num + "\n")
            
            current_stock = 0
            if os.path.exists(DB_FILE):
                with open(DB_FILE, "r") as f:
                    current_stock = len([line for line in f.readlines() if line.strip()])
            
            refresh_btns = [
                ["📥 Upload Numbers (TXT)", "📱 Numbers"],
                [f"📊 Status: {current_stock}", "❌ Clear All Stock"],
                ["🔙 BACK"]
            ]

            success_msg = (
                "<b>╔══════════════════════╗</b>\n"
                '<b> <tg-emoji emoji-id="6232999738459823976">✅</tg-emoji> UPLOAD SUCCESS </b>\n'
                "<b>╚══════════════════════╝</b>\n\n"
                f'<tg-emoji emoji-id="6233241506463883080">📊</tg-emoji> <b>Total Added:</b> <code>{len(cleaned_numbers)}</code>\n'
                '<tg-emoji emoji-id="5345905193005371012">⚡️</tg-emoji> <i>System Ready</i>'
            )
            return await update.message.reply_text(success_msg, parse_mode="HTML", reply_markup=get_job_keyboard(refresh_btns))
        
        # ✅ ভুল ফরম্যাট হ্যান্ডলিং (এটি আগে ছিল না)
        else:
            return await update.message.reply_text(
                '<b>╔══════════════════════╗</b>\n'
                '<b> <tg-emoji emoji-id="6230838059944909526">❌</tg-emoji> INVALID FILE </b>\n'
                '<b>╚══════════════════════╝</b>\n\n'
                '<b>Error:</b> <i>Only .txt files are allowed!</i>',
                parse_mode="HTML"
            )


    # ২. সব নম্বর সরাসরি ডিলিট করার লজিক
    if text == "🗑 Clear All Stock" or text == "❌ Clear All Stock":
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
        
        zero_btns = [
            ["📥 Upload Numbers (TXT)", "📱 Numbers"],
            ["📊 Status: 0", "❌ Clear All Stock"],
            ["🔙 BACK"]
        ]
        
        clear_msg = (
            "<b>╔══════════════════════╗</b>\n"
            '<b> <tg-emoji emoji-id="6230838059944909526">❌</tg-emoji> DATA CLEARED </b>\n'
            "<b>╚══════════════════════╝</b>\n\n"
            '<tg-emoji emoji-id="6230838059944909526">❌</tg-emoji> <b>All OTP removed</b>'
        )
        return await update.message.reply_text(clear_msg, parse_mode="HTML", reply_markup=get_job_keyboard(zero_btns))

    # স্টক রিড করা
    stock_numbers = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            stock_numbers = [line.strip() for line in f.readlines() if line.strip()]
    stock_count = len(stock_numbers)

    # মেইন মেনু বাটন লিস্ট
    main_job_btns = [
        ["📥 Upload Numbers (TXT)", "📱 Numbers"],
        [f"📊 Status: {stock_count}", "❌ Clear All Stock"],
        ["🔙 BACK"]
    ]

    # ৩. নম্বর নেওয়া বা চেঞ্জ করার লজিক
    if text == "🎁 Get One Number" or text == "change_num" or text == "📱 Numbers":
        if stock_count > 0:
            target_number = stock_numbers[0]
            remaining_numbers = stock_numbers[1:]
            
            with open(DB_FILE, "w") as f:
                for num in remaining_numbers:
                    f.write(num + "\n")
            
            with open(USED_FILE, "a") as f:
                f.write(target_number + "\n")

            msg_text = (
                "<b>╔══════════════════════╗</b>\n"
                '<b> <tg-emoji emoji-id="6233241506463883080">📊</tg-emoji> MY STATS </b>\n'
                "<b>╚══════════════════════╝</b>\n\n"
                f'<tg-emoji emoji-id="6233111716847165087">✅</tg-emoji> <b>আপনার নম্বর:</b> <code>{target_number}</code>\n'
                f'<tg-emoji emoji-id="6233241506463883080">📊</tg-emoji> <b>Remaining OTP:</b> <code>{len(remaining_numbers)}</code>'
            )

            inline_kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Change Number", callback_data="change_num")]])
            updated_btns = [
                ["📥 Upload Numbers (TXT)", "📱 Numbers"],
                [f"📊 Status: {len(remaining_numbers)}", "❌ Clear All Stock"],
                ["🔙 BACK"]
            ]

            if is_callback:
                return await query.edit_message_text(msg_text, parse_mode="HTML", reply_markup=inline_kb)
            else:
                return await update.message.reply_text(msg_text, parse_mode="HTML", reply_markup=get_job_keyboard(updated_btns))
        else:
            msg_empty = '<tg-emoji emoji-id="6230838059944909526">❌</tg-emoji> <b>No Number available</b>'
            if is_callback: 
                return await query.edit_message_text(msg_empty, parse_mode="HTML")
            else: 
                return await update.message.reply_text(msg_empty, parse_mode="HTML", reply_markup=get_job_keyboard(main_job_btns))

    # ৪. বাকি বাটনগুলো
    if text == "📥 Upload Numbers (TXT)":
        upload_msg = (
            "<b>╔══════════════════════╗</b>\n"
            '<b> <tg-emoji emoji-id="5296369303661067030">📤</tg-emoji> UPLOAD MODE </b>\n'
            "<b>╚══════════════════════╝</b>\n\n"
            '<tg-emoji emoji-id="5345905193005371012">⚡️</tg-emoji> <b>Status:</b> <i>Waiting...</i>\n'
            '<tg-emoji emoji-id="5433614747381538714">📌</tg-emoji> <i>Upload your .txt file now</i>'
        )
        return await update.message.reply_text(upload_msg, parse_mode="HTML", reply_markup=get_job_keyboard(main_job_btns))

    if text and "📊 Status" in text:
        used_count = 0
        if os.path.exists(USED_FILE):
            with open(USED_FILE, "r") as f:
                used_count = len([l for l in f.readlines() if l.strip()])
        
        report = (
            "<b>╔══════════════════════╗</b>\n"
            '<b> <tg-emoji emoji-id="6206505206197261313">📊</tg-emoji> JOB NUMBER REPORT </b>\n'
            "<b>╚══════════════════════╝</b>\n\n"
            f'<tg-emoji emoji-id="6233111716847165087">✅</tg-emoji> <b>Available:</b> <code>{stock_count}</code>\n'
            f'<tg-emoji emoji-id="6230838059944909526">🚫</tg-emoji> <b>Used Stock:</b> <code>{used_count}</code>\n'
            "━━━━━━━━━━━━━━━━━━━━━\n"
            '<tg-emoji emoji-id="5345905193005371012">⚡️</tg-emoji> <i>System Online & Ready</i>'
        )
        return await update.message.reply_text(report, parse_mode="HTML", reply_markup=get_job_keyboard(main_job_btns))

    if text == "📱 NUMBERS":
        vip_welcome = (
            "<b>╔══════════════════════╗</b>\n"
            '<b> <tg-emoji emoji-id="6231224366483384495">❤️‍🔥</tg-emoji> JOB NUMBER SYSTEM </b>\n'
            "<b>╚══════════════════════╝</b>\n\n"
            '<tg-emoji emoji-id="6230908351379675834">📌</tg-emoji> <b>Welcome to Premium Panel</b>\n'
            '<tg-emoji emoji-id="6230809013081086802">👨‍💻</tg-emoji> <i>Managed by Sadhan Chakma</i>'
        )
        return await update.message.reply_text(vip_welcome, parse_mode="HTML", reply_markup=get_job_keyboard(main_job_btns))

    # BACK লজিক
    if text == "🔙 BACK":
        context.user_data.clear()
        home_btns = [["📲 OTP MANAGER", "📧 EMAIL TOOL"], ["📞 NUMBER TOOL", "🔁 REPEAT TOOL"],["🔍 SEARCH COUNTRY"], ["ℹ️ HELP"]]
        back_msg = '<tg-emoji emoji-id="5260433458324322750">🔙</tg-emoji> <b>Back to Main Menu</b>'
        return await update.message.reply_text(back_msg, parse_mode="HTML", reply_markup=get_job_keyboard(home_btns))
