# 🤖 GeminiVision Bot

<div align="center">

![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?style=for-the-badge&logo=telegram)
![Google Gemini](https://img.shields.io/badge/Google-Gemini-red?style=for-the-badge&logo=google)

A powerful Telegram bot powered by Google's Gemini AI that can understand both text and images! 🚀

[Features](#✨-features) • [Installation](#🛠️-installation) • [Usage](#📱-usage) • [Configuration](#⚙️-configuration) • [Examples](#📸-examples)

</div>

---

## ✨ Features

- 🤖 **Advanced AI Conversations**: Engage in natural conversations with Google's latest Gemini AI
- 🖼️ **Image Analysis**: Send images and get detailed analysis and insights
- 🎯 **Multi-Purpose**: Can answer questions, analyze images, explain concepts, and more
- ⚡ **Fast Responses**: Uses Gemini's flash model for quick text responses
- 🔍 **Detailed Vision Analysis**: Powered by Gemini Pro Vision for image understanding
- 🎨 **Beautiful Formatting**: Clean and organized responses with relevant emojis

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/geminivision-bot.git
   cd geminivision-bot
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual API keys
   ```

## ⚙️ Configuration

1. **Get your API Keys**:
   - Telegram Bot Token: Message [@BotFather](https://t.me/botfather) on Telegram
   - Gemini API Key: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)

2. **Update your .env file**:
   ```env
   BOT_TOKEN=your_telegram_bot_token
   GEMINI_API_KEY=your_gemini_api_key
   ```

## 📱 Usage

### Text Queries
Send text messages to the bot using the `/ai` command:
```
/ai What is quantum computing?
```

### Image Analysis
Two ways to analyze images:

1. **Send image with caption**:
   - Send an image to the bot
   - Add your question as the caption

2. **Reply to image**:
   - Send an image
   - Reply to it with `/ai` and your question

## 📸 Examples

### Text Analysis
```
You: /ai Explain blockchain technology
Bot: 🔑 Key Features:
    • Decentralized ledger
    • Immutable records
    • Cryptographic security
    
⚙️ How it Works:
    • Transactions are verified
    • Blocks are created
    • Chain is maintained
```

### Image Analysis
```
You: *sends food image* "What ingredients do I need?"
Bot: 📝 Recipe Components:
    • Lists main ingredients
    • Cooking instructions
    • Time and servings
```

## 🔒 Security

- Never share your API keys
- Store sensitive data in .env file
- Keep your bot token private
- Regularly update dependencies

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

<!-- ## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. -->

---

<div align="center">

Made with ❤️ by [Ahmed]

</div>
