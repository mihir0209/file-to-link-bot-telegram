from dotenv import load_dotenv
import os
import requests
import traceback
from urllib.parse import quote_plus
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Helper function for MarkdownV2 escaping
def escape_md(text):
    """Escape special characters for Telegram MarkdownV2."""
    escape_chars = r'_[]()~`>#+-=|{}.!'
    return ''.join('\\' + c if c in escape_chars else c for c in str(text))

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CDN_ACCESS_TOKEN = os.getenv("CDN_ACCESS_TOKEN")
CDN_UPLOAD_URL = "https://upload.snapzion.com/api/public-upload"
WEB_PLAYER_BASE = os.getenv("WEB_PLAYER_BASE", "https://filetolink-stream.vercel.app/player")  # Update to your Vercel URL

# Navigation keyboard
main_keyboard = ReplyKeyboardMarkup(
    [["Send File"], ["/help"]],
    resize_keyboard=True
)

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 *Welcome to FileToLink Bot\\!* \n\n"
        "📤 _Send me an image or video, and I’ll upload it to the CDN and provide you with:_\n"
        "• A direct download link\n"
        "• An online streaming link \\(with built\\-in player\\)\n"
        "• Links to open in external players \\(MX Player, Playit on Android\\)\n\n"
        "Type /help for more info\\."
    )
    await update.message.reply_text(welcome_text, parse_mode="MarkdownV2", reply_markup=main_keyboard)

# /help command handler
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "ℹ️ *How to use FileToLink Bot:*\n\n"
        "1️⃣ *Send* an image or video file\\.\n"
        "2️⃣ *Get* a direct CDN download link\\.\n"
        "3️⃣ *Get* an online player link for instant streaming\\.\n"
        "4️⃣ *Get* links for external players \\(MX Player, Playit on Android\\)\\.\n\n"
        "*Supported formats:* MP4, JPG, PNG, etc\\.\n"
        "For any issues, contact @YourSupportHandle\\."
    )
    await update.message.reply_text(help_text, parse_mode="MarkdownV2", reply_markup=main_keyboard)

# File handler
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Get the file (document, photo, or video)
        file = (
            update.message.document or
            (update.message.photo[-1] if update.message.photo else None) or
            update.message.video
        )
        if not file:
            await update.message.reply_text(
                "❗ Please send an image or video file\\.",
                parse_mode="MarkdownV2",
                reply_markup=main_keyboard
            )
            return

        # Download the file locally
        file_obj = await file.get_file()
        file_path = await file_obj.download_to_drive()
        file_name = file.file_name if hasattr(file, "file_name") else os.path.basename(file_path)

        # Determine file type with fallback
        if update.message.photo:
            file_type = "image/jpeg"
            file_name = file_name or "photo.jpg"
        elif update.message.video:
            file_type = "video/mp4"
            file_name = file_name or "video.mp4"
        elif update.message.document and update.message.document.mime_type:

            file_type = update.message.document.mime_type
            file_name = file_name or update.message.document.file_name or "document"
        else:
            file_type = "application/octet-stream"
            file_name = file_name or "file"

        # Upload to CDN
        with open(file_path, "rb") as f:
            response = requests.post(
                CDN_UPLOAD_URL,
                headers={"Authorization": f"Bearer {CDN_ACCESS_TOKEN}"},
                files={"file": (file_name, f, file_type)}
            )
        os.remove(file_path)  # Clean up local file

        if response.status_code == 200:
            data = response.json()
            cdn_url = data.get("url")
            if not cdn_url:
                raise Exception("CDN did not return a valid URL.")

            # Ensure CDN URL uses HTTPS
            if not cdn_url.startswith("https://"):
                cdn_url = cdn_url.replace("http://", "https://")

            # Generate all links
            player_url = f"{WEB_PLAYER_BASE}?url={quote_plus(cdn_url)}"
            mxplayer_link = f"intent:{cdn_url}#Intent;package=com.mxtech.videoplayer.ad;type=video/mp4;S.title={quote_plus(file_name)};end"
            playit_link = f"playit://video?url={quote_plus(cdn_url)}&title={quote_plus(file_name)}"

            # Prepare response text (escape only non-URL text)
            reply_text = (
                "✅ *Your file is ready\\!*\n\n"
                f"• [Direct Download]({cdn_url})\n"
                f"• [Watch Online]({player_url})\n\n"
                "Or open in your favorite external player:"
            )

            # Inline buttons (URLs don't need escaping here)
            buttons = [
                [InlineKeyboardButton("⬇️ Direct Download", url=cdn_url)],
                [InlineKeyboardButton("▶️ Watch Online", url=player_url)],
            ]
            markup = InlineKeyboardMarkup(buttons)

            await update.message.reply_text(
                reply_text,
                parse_mode="MarkdownV2",
                disable_web_page_preview=True,
                reply_markup=markup
            )
        else:
            error_text = (
                f"❗ *Upload failed\\.*\n"
                f"Status code: {response.status_code}\n"
                f"Response: {escape_md(response.text[:200])}"  # Limit response length for safety
            )
            print(f"CDN Upload Error: {response.status_code} - {response.text}")
            await update.message.reply_text(error_text, parse_mode="MarkdownV2", reply_markup=main_keyboard)

    except Exception as e:
        error_msg = str(e)[:200]  # Limit error message length
        print(f"Error: {traceback.format_exc()}")
        await update.message.reply_text(
            f"❗ *An error occurred:*\n`{escape_md(error_msg)}`",
            parse_mode="MarkdownV2",
            reply_markup=main_keyboard
        )

# Main function
def main():
    if not BOT_TOKEN:
        raise Exception("BOT_TOKEN is missing! Check your .env file.")
    if not CDN_ACCESS_TOKEN:
        raise Exception("CDN_ACCESS_TOKEN is missing! Check your .env file.")
    # if not WEB_PLAYER_BASE.startswith("https://"):
    #     raise Exception("WEB_PLAYER_BASE must use HTTPS! Update your .env file.")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO | filters.VIDEO, handle_file))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()