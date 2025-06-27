import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, ContextTypes
from dotenv import load_dotenv
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Set this in your .env or environment
CDN_UPLOAD_URL = "https://upload.snapzion.com/api/public-upload"
CDN_ACCESS_TOKEN = os.getenv("CDN_ACCESS_TOKEN")  # Set this in your .env or environment

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me an image or video and I'll upload it to the CDN!")
import traceback

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        file = update.message.document or (update.message.photo[-1] if update.message.photo else None) or update.message.video
        if not file:
            await update.message.reply_text("Please send an image or video file.")
            return

        file_obj = await file.get_file()
        file_path = await file_obj.download_to_drive()
        
        # Guess file type
        if update.message.photo:
            file_type = "image/jpeg"  # Telegram usually sends JPEG for photos
        elif update.message.video:
            file_type = "video/mp4"
        elif update.message.document and update.message.document.mime_type:
            file_type = update.message.document.mime_type
        else:
            file_type = "application/octet-stream"

        with open(file_path, "rb") as f:
            response = requests.post(
                CDN_UPLOAD_URL,
                headers={"Authorization": f"Bearer {CDN_ACCESS_TOKEN}"},
                files={"file": (os.path.basename(file_path), f, file_type)}
            )
        os.remove(file_path)

        if response.status_code == 200:
            cdn_url = response.json().get("url")
            await update.message.reply_text(f"Here is your CDN link: {cdn_url}")
        else:
            # Debug info for failed upload
            error_text = (
                f"Upload failed.\n"
                f"Status code: {response.status_code}\n"
                f"Response: {response.text}"
            )
            print(error_text)
            await update.message.reply_text(error_text)

    except Exception as e:
        # Print full traceback to the console for developer
        traceback.print_exc()
        # Send error message to the user
        await update.message.reply_text(f"An error occurred:\n{str(e)}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()  # Loads CDN_ACCESS_TOKEN from .env

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO | filters.VIDEO, handle_file))
    app.run_polling()
