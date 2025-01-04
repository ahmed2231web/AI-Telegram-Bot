import os
import logging
import time
import sys
import socket
import re
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)
from gemini_stream import stream_gemini_response

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def is_bot_running():
    """Check if another instance of the bot is running"""
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.bind('\0telegram_bot_lock')  # Abstract socket
        return False
    except socket.error:
        return True

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    welcome_message = (
        "👋 Welcome to the Gemini AI Chatbot!\n\n"
        "Use the /ai command followed by your message to chat with me.\n"
        "Example: <code>/ai Explain blockchain technology</code>\n\n"
        "I'll provide well-structured responses with clear sections! 🚀"
    )
    await update.message.reply_text(welcome_message, parse_mode='HTML')

def add_emojis(text: str) -> str:
    """Add emojis to section headers."""
    headers = {
        "Key Features": "🔑",
        "How it Works": "⚙️",
        "Benefits": "✨",
        "Applications": "🚀",
        "Example": "📝",
        "Summary": "📌",
        "Steps": "📋",
        "Important": "❗",
        "Note": "📢",
        "Tips": "💡"
    }
    
    lines = []
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        # Add emojis to headers
        for header, emoji in headers.items():
            if line.lower().startswith(f"{header.lower()}:"):
                line = f"{emoji} {line}"
                break
            
        lines.append(line)
    
    return '\n'.join(lines)

async def ai_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /ai command and get responses from Gemini API."""
    if not context.args:
        await update.message.reply_text(
            "Please provide a message after the /ai command.\n"
            "Example: /ai Explain blockchain technology"
        )
        return

    user_message = " ".join(context.args)
    
    # Add a length check to prevent very long messages
    if len(user_message) > 1000:
        await update.message.reply_text(
            "Your message is too long. Please keep it under 1000 characters."
        )
        return
        
    processing_message = await update.message.reply_text(
        "🤔 Processing your request..."
    )
    
    try:
        # Get the response from Gemini API
        for response in stream_gemini_response(GEMINI_API_KEY, user_message):
            try:
                # Add emojis to the response
                formatted_response = add_emojis(response)
                
                # Split long messages if they exceed Telegram's limit
                if len(formatted_response) > 4000:
                    chunks = [formatted_response[i:i+4000] for i in range(0, len(formatted_response), 4000)]
                    # Edit the first message with the first chunk
                    await processing_message.edit_text(chunks[0])
                    # Send remaining chunks as new messages
                    for chunk in chunks[1:]:
                        await update.message.reply_text(chunk)
                else:
                    await processing_message.edit_text(formatted_response)
            except Exception as e:
                logger.error(f"Error sending message: {e}")
                # If editing fails, send as a new message
                await update.message.reply_text(formatted_response)
            
    except Exception as e:
        logger.error(f"Error in ai_command: {e}")
        await processing_message.edit_text(
            "❌ Sorry, I encountered an error while processing your request. Please try again later."
        )

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle images sent to the bot."""
    # Check if there's a caption
    if not update.message.caption:
        await update.message.reply_text(
            "Please provide a caption with your image describing what you'd like to know about it."
        )
        return

    # Get the image file
    photo = update.message.photo[-1]  # Get the largest size
    image_file = await context.bot.get_file(photo.file_id)
    
    # Create a temporary directory if it doesn't exist
    import os
    temp_dir = os.path.join(os.getcwd(), "temp")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    # Download the image
    image_path = os.path.join(temp_dir, f"{photo.file_id}.jpg")
    await image_file.download_to_drive(image_path)
    
    processing_message = await update.message.reply_text(
        "🤔 Analyzing your image..."
    )
    
    try:
        # Get response from Gemini API with the image
        for response in stream_gemini_response(GEMINI_API_KEY, update.message.caption, image_path):
            try:
                # Add emojis to the response
                formatted_response = add_emojis(response)
                
                # Split long messages if they exceed Telegram's limit
                if len(formatted_response) > 4000:
                    chunks = [formatted_response[i:i+4000] for i in range(0, len(formatted_response), 4000)]
                    await processing_message.edit_text(chunks[0])
                    for chunk in chunks[1:]:
                        await update.message.reply_text(chunk)
                else:
                    await processing_message.edit_text(formatted_response)
            except Exception as e:
                logger.error(f"Error sending message: {e}")
                await update.message.reply_text(formatted_response)
    except Exception as e:
        logger.error(f"Error in handle_image: {e}")
        await processing_message.edit_text(
            "❌ Sorry, I encountered an error while processing your image. Please try again later."
        )
    finally:
        # Clean up - remove the temporary image file
        try:
            os.remove(image_path)
        except Exception as e:
            logger.error(f"Error removing temporary file: {e}")

def main() -> None:
    """Start the bot."""
    # Check for required environment variables
    if not TELEGRAM_BOT_TOKEN or not GEMINI_API_KEY:
        logger.error("Missing required environment variables. Please check your .env file.")
        return

    # Check if bot is already running
    if is_bot_running():
        logger.error("Another instance of the bot is already running!")
        sys.exit(1)

    try:
        # Create the Application
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

        # Add command handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("ai", ai_command))

        # Add message handlers
        application.add_handler(MessageHandler(filters.PHOTO, handle_image))

        # Start the Bot
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
