import os
from telegram import Update
from telegram.ext import ContextTypes

# ✅ ডাটাবেস সার্চ ফাংশন
def search_country_in_file(query):
    query = query.strip().lower()
    results = []
    file_path = 'all_countries_short_codes.txt'
    
    if not os.path.exists(file_path):
        return "error_file_missing"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if query in line.lower():
                    results.append(line.strip())
        return results
    except Exception:
        return "error_system"

# ✅ প্রফেশনাল কান্ট্রি সার্চ হ্যান্ডলার (Emoji-Free / Error-Safe)
async def country_search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text
    mode = context.user_data.get("mode")

    # ১. মেইন বাটন ক্লিক করলে
    if text == "🔍 SEARCH COUNTRY":
        context.user_data["mode"] = "search_country"
        
        msg = (
            "<b>╔══════════════════════╗</b>\n"
            "<b>   🌍 COUNTRY SEARCH 🌍   </b>\n"
            "<b>╚══════════════════════╝</b>\n\n"
            "<b>Status:</b> <code>Active Mode</code>\n"
            "<i>অনুগ্রহ করে দেশের নাম বা শর্ট কোড পাঠান।</i>\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "<b>উদাহরণ:</b> <code>Bangladesh</code> বা <code>BD</code>"
        )
        return await update.message.reply_text(msg, parse_mode="HTML")

    # ২. ইনপুট মোড
    if mode == "search_country":
        # মেইন বাটন টিপলে মোড অফ হবে
        main_buttons = ["📲 OTP MANAGER", "📧 EMAIL TOOL", "📞 NUMBER TOOL", "🔁 REPEAT TOOL", "📱 NUMBERS", "ℹ️ HELP", "🔙 BACK"]
        if text in main_buttons:
            context.user_data["mode"] = None
            return 

        found_list = search_country_in_file(text)
        
        if found_list == "error_file_missing":
            return await update.message.reply_text("❌ <b>Error:</b> Database file missing!", parse_mode="HTML")
        
        if found_list == "error_system":
            return await update.message.reply_text("⚠️ <b>System Error!</b>", parse_mode="HTML")

        if found_list:
            # রেজাল্ট লিস্ট তৈরি (সিম্পল ইমোজি দিয়ে)
            res_text = ""
            for res in found_list:
                res_text += f"📍 <code>{res}</code>\n"
            
            response = (
                "<b>╔══════════════════════╗</b>\n"
                "<b>   ✅ MATCH FOUND! ✅   </b>\n"
                "<b>╚══════════════════════╝</b>\n\n"
                f"{res_text}"
                "━━━━━━━━━━━━━━━━━━━━━\n"
                "<i>Tap to copy the code easily.</i>"
            )
            await update.message.reply_text(response, parse_mode="HTML")
        else:
            error_msg = (
                "❌ <b>NO MATCH FOUND!</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━\n"
                f"দুঃখিত, <code>{text}</code> পাওয়া যায়নি।"
            )
            await update.message.reply_text(error_msg, parse_mode="HTML")
