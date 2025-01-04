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
from crypto_utils import CryptoAnalyzer

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "").strip()

# Debug logging
print("Environment Variables Status:")
print(f"BOT_TOKEN: {'✓ Set' if BOT_TOKEN else '✗ Missing'} (Length: {len(BOT_TOKEN) if BOT_TOKEN else 0})")
print(f"GEMINI_API_KEY: {'✓ Set' if GEMINI_API_KEY else '✗ Missing'} (Length: {len(GEMINI_API_KEY) if GEMINI_API_KEY else 0})")
print(f"ALPHA_VANTAGE_API_KEY: {'✓ Set' if ALPHA_VANTAGE_API_KEY else '✗ Missing'} (Length: {len(ALPHA_VANTAGE_API_KEY) if ALPHA_VANTAGE_API_KEY else 0})")

if not all([BOT_TOKEN, GEMINI_API_KEY, ALPHA_VANTAGE_API_KEY]):
    print("Error: Missing required environment variables. Please check your .env file.")
    sys.exit(1)

# Initialize CryptoAnalyzer
try:
    crypto = CryptoAnalyzer()
except ValueError as e:
    print(f"Error initializing CryptoAnalyzer: {e}")
    print(f"ALPHA_VANTAGE_API_KEY value: '{ALPHA_VANTAGE_API_KEY}'")
    sys.exit(1)

# Define available symbols and timeframes
CRYPTO_SYMBOLS = {
    "BTC": "BTC",
    "ETH": "ETH",
    "SOL": "SOL",
    "ADA": "ADA",
    "DOGE": "DOGE",
    "XRP": "XRP",
    "LTC": "LTC",
    "BNB": "BNB",
    "MATIC": "MATIC",
    "DOT": "DOT"
}

TIME_FRAMES = ["1day", "1week", "1month"]

def is_bot_running():
    """Check if another instance of the bot is running"""
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.bind('\0telegram_bot_lock')  # Abstract socket
        return False
    except socket.error:
        return True

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when the command /start is issued."""
    welcome_message = """
🌟 *Welcome to GeminiVision Bot!* 🌟

Your all-in-one AI assistant for crypto insights and image analysis! 🤖✨

🎯 *What I Can Do:*

🧠 *AI Powers*
• `/ai [question]` - Ask me anything! I'm powered by Google's Gemini AI
• 📸 Send any image with a caption - I'll analyze it for you!

📊 *Crypto Commands*
• `/price [symbol]` - Real-time crypto prices
• `/chart [symbol] [timeframe]` - Beautiful price charts

🪙 *Supported Cryptocurrencies:*
`BTC` `ETH` `SOL` `ADA` `DOGE` `XRP` `LTC` `BNB` `MATIC` `DOT`

⏱ *Chart Timeframes:*
`1day` `1week` `1month`

🚀 *Try These:*
1️⃣ `/ai Tell me about NFTs`
2️⃣ `/price ETH`
3️⃣ `/chart BTC 1week`

Let's explore the future of technology together! 🌐✨
"""
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

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

async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Get the current price of a cryptocurrency."""
    if not context.args:
        symbols_list = ", ".join(f"`{s}`" for s in CRYPTO_SYMBOLS.keys())
        await update.message.reply_text(
            f"Please provide a cryptocurrency symbol.\nAvailable symbols: {symbols_list}\nExample: `/price BTC`",
            parse_mode='Markdown'
        )
        return

    symbol = context.args[0].upper()
    if symbol not in CRYPTO_SYMBOLS:
        symbols_list = ", ".join(f"`{s}`" for s in CRYPTO_SYMBOLS.keys())
        await update.message.reply_text(
            f"❌ Invalid symbol.\nAvailable symbols: {symbols_list}",
            parse_mode='Markdown'
        )
        return

    # Send initial message
    message = await update.message.reply_text("💰 Fetching price data...")

    try:
        price = crypto.get_crypto_price(symbol)
        if price is not None:
            await message.edit_text(
                f"💰 *{symbol}/USD*\nPrice: `${price:,.2f}`",
                parse_mode='Markdown'
            )
        else:
            await message.edit_text("❌ Unable to fetch price data. Please try again later.")
    except Exception as e:
        logger.error(f"Error in price command: {e}")
        await message.edit_text("❌ Error fetching price data. Please try again later.")

async def chart_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate and send a price chart."""
    if len(context.args) < 2:
        timeframes_list = ", ".join(f"`{t}`" for t in TIME_FRAMES)
        symbols_list = ", ".join(f"`{s}`" for s in CRYPTO_SYMBOLS.keys())
        await update.message.reply_text(
            f"Please provide both symbol and timeframe.\n"
            f"Available symbols: {symbols_list}\n"
            f"Available timeframes: {timeframes_list}\n"
            "Example: `/chart BTC 1day`",
            parse_mode='Markdown'
        )
        return

    symbol = context.args[0].upper()
    timeframe = context.args[1].lower()

    if symbol not in CRYPTO_SYMBOLS:
        symbols_list = ", ".join(f"`{s}`" for s in CRYPTO_SYMBOLS.keys())
        await update.message.reply_text(
            f"❌ Invalid symbol.\nAvailable symbols: {symbols_list}",
            parse_mode='Markdown'
        )
        return

    if timeframe not in TIME_FRAMES:
        timeframes_list = ", ".join(f"`{t}`" for t in TIME_FRAMES)
        await update.message.reply_text(
            f"❌ Invalid timeframe.\nAvailable timeframes: {timeframes_list}",
            parse_mode='Markdown'
        )
        return

    # Send initial message
    message = await update.message.reply_text("📊 Generating chart...")

    try:
        chart_buffer = crypto.generate_price_chart(symbol, timeframe)
        if chart_buffer:
            await message.delete()
            await update.message.reply_photo(
                photo=chart_buffer,
                caption=f"📈 {symbol}/USD Price Chart ({timeframe})"
            )
        else:
            await message.edit_text("❌ Unable to generate chart. Please try again later.")
    except Exception as e:
        logger.error(f"Error in chart command: {e}")
        await message.edit_text("❌ Error generating chart. Please try again later.")

def main() -> None:
    """Start the bot."""
    try:
        # Create the Application
        application = Application.builder().token(BOT_TOKEN).build()

        # Add command handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("ai", ai_command))
        application.add_handler(CommandHandler("price", price_command))
        application.add_handler(CommandHandler("chart", chart_command))

        # Add message handlers
        application.add_handler(MessageHandler(filters.PHOTO, handle_image))

        # Set higher timeout for long polling
        application.run_polling(timeout=30, drop_pending_updates=True)
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
