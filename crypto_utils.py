import os
import logging
import requests
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Alpha Vantage API configuration
ALPHA_VANTAGE_API_URL = "https://www.alphavantage.co/query"

class CryptoAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        if not self.api_key:
            raise ValueError("ALPHA_VANTAGE_API_KEY environment variable is not set")

    def get_crypto_price(self, symbol):
        """Get current price for a cryptocurrency."""
        try:
            params = {
                "function": "DIGITAL_CURRENCY_DAILY",
                "symbol": symbol,
                "market": "USD",
                "apikey": self.api_key
            }
            
            response = requests.get(ALPHA_VANTAGE_API_URL, params=params)
            data = response.json()
            
            if "Error Message" in data:
                logger.error(f"API error: {data['Error Message']}")
                return None
            elif "Note" in data:
                logger.warning(f"API limit reached: {data['Note']}")
                return None
            
            time_series = data.get("Time Series (Digital Currency Daily)")
            if time_series:
                latest_date = list(time_series.keys())[0]
                latest_data = time_series[latest_date]
                return float(latest_data["4. close"])
            
            logger.error("Unexpected API response format")
            return None
            
        except Exception as e:
            logger.error(f"Error fetching price: {str(e)}")
            return None

    def generate_price_chart(self, symbol, timeframe):
        """Generate a price chart for a cryptocurrency."""
        try:
            # Get historical data
            params = {
                "function": "DIGITAL_CURRENCY_DAILY",
                "symbol": symbol,
                "market": "USD",
                "apikey": self.api_key
            }
            
            response = requests.get(ALPHA_VANTAGE_API_URL, params=params)
            data = response.json()
            
            if "Error Message" in data:
                logger.error(f"API error: {data['Error Message']}")
                return None
            elif "Note" in data:
                logger.warning(f"API limit reached: {data['Note']}")
                return None
                
            time_series = data.get("Time Series (Digital Currency Daily)")
            if not time_series:
                logger.error("No time series data in response")
                return None

            # Convert to DataFrame
            df = pd.DataFrame.from_dict(time_series, orient='index')
            
            # Debug log the columns
            logger.info(f"Available columns: {df.columns.tolist()}")
            
            # Rename columns for mplfinance
            column_map = {
                "1. open": "Open",
                "2. high": "High",
                "3. low": "Low",
                "4. close": "Close",
                "5. volume": "Volume"
            }
            
            df = df[list(column_map.keys())]  # Select only needed columns
            df = df.rename(columns=column_map)  # Rename columns
            
            # Convert to numeric and handle any missing values
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Convert index to datetime and sort
            df.index = pd.to_datetime(df.index)
            df = df.sort_index()
                
            # Filter data based on timeframe
            if timeframe == "1day":
                df = df.tail(24)
            elif timeframe == "1week":
                df = df.tail(7)
            elif timeframe == "1month":
                df = df.tail(30)
                
            # Create chart
            plt.style.use('dark_background')
            fig, axlist = mpf.plot(
                df,
                type='candle',
                volume=True,
                title=f'{symbol}/USD Price Chart ({timeframe})',
                ylabel='Price (USD)',
                style='charles',
                figsize=(10, 6),
                returnfig=True
            )
            
            # Save to buffer
            buffer = BytesIO()
            fig.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0.2)
            buffer.seek(0)
            plt.close('all')
            
            return buffer
            
        except Exception as e:
            logger.error(f"Error generating chart: {str(e)}")
            return None