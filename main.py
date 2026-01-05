import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")
GROUP_USERNAME = "@CraftToSurviveMM"

VERSION_LINK = "https://example.com/version"
SERVER_LINK  = "https://example.com/server"
DISCORD_LINK = "https://discord.gg/yourlink"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("🔗 GP Join ပေးပါ", url=f"https://t.me/{GROUP_USERNAME.replace('@','')}")],
        [InlineKeyboardButton("✅ Join ပြီးပါပြီ", callback_data="check_join")]
    ]
    await update.message.reply_text(
        "🎉 Welcome!\nအရင်ဆုံး Group ကို Join ပေးပါ 👇",
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def show_menu(query):
    kb = [
        [InlineKeyboardButton("📦 Version Link", url=VERSION_LINK)],
        [InlineKeyboardButton("🌐 Server Link",  url=SERVER_LINK)],
        [InlineKeyboardButton("💬 Discord Link", url=DISCORD_LINK)],
    ]
    await query.edit_message_text(
        "✅ Join ပြီးပါပြီ\nMenu ထဲက ရွေးပါ 👇",
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    try:
        member = await context.bot.get_chat_member(GROUP_USERNAME, uid)
        if member.status in ("member", "administrator", "creator"):
            await show_menu(query)
        else:
            await query.edit_message_text("❌ Group Join မလုပ်ရသေးပါ")
    except:
        await query.edit_message_text("⚠️ Bot ကို Group ထဲ Admin အဖြစ် ထည့်ထားပါ")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))

print("Bot is running...")
app.run_polling()
