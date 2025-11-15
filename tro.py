import asyncio
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    ContextTypes,
)

# ==============================
# SETTINGS
# ==============================
TOKEN = "7571535805:AAGDJBJqzuytpjpce9ivNG6eAUaRTYeQBuY"
VOTE_LINK = "https://cr7.soltrendingvote.top"
IMAGE_URL = "https://icohtech.ng/cr7.jpg"
GROUP_CHAT_ID = -1003295107465

# Track group users
group_members = set()

# ==============================
# WELCOME HANDLER
# ==============================
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.new_chat_members:
        return

    for member in update.message.new_chat_members:
        username = member.username or member.first_name
        group_members.add(username)

        caption = f"""
🚀 OFFICIAL $TROLL AIRDROP IS LIVE

Attention @{username},
The $TROLL airdrop claim window is now open and supplies are strictly limited.

✅ Eligible users can claim their $TROLL allocation now
✅ Distribution is first-come, first-served
✅ Once the pool is filled, the airdrop closes permanently

⚠️ This is the only official claim notice.
No admin will DM you first. Never share your seed phrase or private key.

👇 Tap “Claim Airdrop” below and secure your $TROLL before it’s gone.
"""
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("🚀 CLAIM NOW", url=VOTE_LINK)]]
        )

        await update.message.reply_photo(
            photo=IMAGE_URL,
            caption=caption,
            parse_mode="Markdown",
            reply_markup=button
        )

# ==============================
# REMINDER HANDLER
# ==============================
async def send_reminder(context: ContextTypes.DEFAULT_TYPE):

    base_msg = """⏰ $TROLL AIRDROP – FINAL REMINDER

This is a reminder that the $TROLL airdrop claim is still live, but the remaining allocation is almost filled.

✅ Claim your reserved $TROLL
✅ First-come, first-served
✅ No second round once it’s closed

If you miss this window, you’re out.

👇 Tap “Claim Airdrop” now and secure your $TROLL before the pool is gone.
"""

    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("💰 CLAIM NOW!", url=VOTE_LINK)]]
    )

    members = list(group_members)
    batch_size = 5

    # No tags yet? Send only base message
    if not members:
        await context.bot.send_message(
            GROUP_CHAT_ID,
            base_msg,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
        return

    for i in range(0, len(members), batch_size):
        batch = members[i:i + batch_size]
        tags = ", ".join(f"@{u}" for u in batch)

        msg = f"{base_msg}\n\n{tags}"

        try:
            await context.bot.send_message(
                GROUP_CHAT_ID,
                msg,
                parse_mode="Markdown",
                reply_markup=reply_markup
            )
        except Exception as e:
            print("❌ Reminder error:", e)

        await asyncio.sleep(6)  # flood-safe delay

# ==============================
# MAIN BOT LOOP (FOREVER)
# ==============================
def main():
    print("🤖 CR7 Bot starting (Worker mode, runs forever)...")

    app = ApplicationBuilder().token(TOKEN).build()

    # Welcome messages
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))

    # Reminders every 10 minutes
    app.job_queue.run_repeating(send_reminder, interval=600, first=20)

    # Worker: Run polling forever
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
