<div align="center">

# 🌟 GeminiVision Bot

### Your AI-Powered Telegram Assistant with Vision & Crypto Insights

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white&labelColor=black)](https://www.python.org/downloads/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?style=for-the-badge&logo=telegram&logoColor=white&labelColor=black)](https://t.me/your_bot)
[![Google Gemini](https://img.shields.io/badge/Powered%20by-Gemini%20AI-red?style=for-the-badge&logo=google&logoColor=white&labelColor=black)](https://deepmind.google/technologies/gemini/)
[![Alpha Vantage](https://img.shields.io/badge/Crypto%20Data-Alpha%20Vantage-green?style=for-the-badge&logo=bitcoin&logoColor=white&labelColor=black)](https://www.alphavantage.co/)

---

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-configuration">Configuration</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-examples">Examples</a>
</p>

</div>

## 🎯 Overview

Welcome to GeminiVision Bot – a cutting-edge Telegram bot that combines the power of Google's Gemini AI with real-time cryptocurrency insights. Experience seamless interaction with advanced AI while staying updated with the crypto market! 

### 🌈 Key Highlights

- 🤖 **AI Vision Analysis**: Understand images with Google's latest Gemini Vision AI
- 💰 **Crypto Tracking**: Real-time prices and professional charts
- 🎨 **Beautiful UI**: Clean, emoji-rich responses
- ⚡ **Lightning Fast**: Optimized for quick responses
- 🛡️ **Secure**: Best practices for API key management

## ✨ Features

<details>
<summary>🤖 AI Capabilities</summary>

- Natural language understanding
- Image analysis and description
- Context-aware conversations
- Multi-turn dialogue support
- Rich text formatting
</details>

<details>
<summary>📈 Cryptocurrency Features</summary>

- Real-time price tracking
- Professional candlestick charts
- Multiple timeframe analysis
- Volume indicators
- Top 10 cryptocurrencies support
</details>

<details>
<summary>🛠️ Technical Features</summary>

- Asynchronous processing
- Error handling & recovery
- Rate limit management
- Automatic retries
- Extensive logging
</details>

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/geminivision-bot.git

# Navigate to project
cd geminivision-bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## ⚙️ Configuration

### 1. Get Your API Keys

| API | Purpose | Get Key |
|-----|----------|----------|
| 🤖 Telegram | Bot Token | [@BotFather](https://t.me/botfather) |
| 🧠 Gemini AI | Vision & Text AI | [Google AI Studio](https://makersuite.google.com/app/apikey) |
| 📊 Alpha Vantage | Crypto Data | [Alpha Vantage](https://www.alphavantage.co/support/#api-key) |

### 2. Set Up Environment

```bash
cp .env.example .env
```

Edit `.env` with your API keys:
```env
BOT_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_gemini_api_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
```

## 📱 Usage

### 💬 AI Commands

```bash
/ai What is quantum computing?
/ai Explain blockchain technology
/ai Tell me about SpaceX
```

### 🖼️ Image Analysis

<table>
<tr>
<th>Method</th>
<th>Steps</th>
</tr>
<tr>
<td>With Caption</td>
<td>
1. Send image<br>
2. Add question as caption
</td>
</tr>
<tr>
<td>Reply to Image</td>
<td>
1. Send image<br>
2. Reply with /ai command
</td>
</tr>
</table>

### 💰 Cryptocurrency Commands

#### Price Checking
```bash
/price BTC    # Bitcoin price
/price ETH    # Ethereum price
```

#### Chart Analysis
```bash
/chart BTC 1day    # Daily Bitcoin chart
/chart ETH 1week   # Weekly Ethereum chart
/chart BTC 1month  # Monthly Bitcoin chart
```

### 🪙 Supported Cryptocurrencies

| Symbol | Name | Symbol | Name |
|--------|------|--------|------|
| BTC | Bitcoin | ETH | Ethereum |
| SOL | Solana | ADA | Cardano |
| DOGE | Dogecoin | XRP | Ripple |
| LTC | Litecoin | BNB | Binance Coin |
| MATIC | Polygon | DOT | Polkadot |

### ⏰ Timeframes

- `1day`: 24-hour analysis
- `1week`: 7-day trends
- `1month`: 30-day overview

## 📸 Examples

<details>
<summary>💬 AI Chat Example</summary>

```
You: /ai Explain blockchain
Bot: 🔗 Blockchain Explained:

🏗️ Structure:
• Decentralized digital ledger
• Chain of chronological blocks
• Cryptographically secured

🔑 Key Features:
• Immutable records
• Transparent transactions
• No central authority

💡 Use Cases:
• Cryptocurrencies
• Smart contracts
• Supply chain tracking
```
</details>

<details>
<summary>📊 Crypto Analysis Example</summary>

```
You: /price BTC
Bot: 💰 BTC/USD
Current Price: $97,875.91
Updated: 2025-01-04 22:47 UTC

You: /chart ETH 1week
Bot: 📈 Generating Ethereum weekly chart...
*Sends professional candlestick chart*
```
</details>

## 🛡️ Security

- ✅ Environment variables for API keys
- 🔒 Secure error handling
- 🔐 Rate limiting protection
- 📝 Extensive logging
- 🚫 Input validation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
---

<div align="center">

### Made with ❤️ using Google Gemini AI and Alpha Vantage

[![Stars](https://img.shields.io/github/stars/yourusername/geminivision-bot?style=social)](https://github.com/yourusername/geminivision-bot/stargazers)
[![Follow](https://img.shields.io/github/followers/yourusername?style=social)](https://github.com/yourusername)

</div>
