import logging
from typing import Generator, Optional
import google.generativeai as genai
from PIL import Image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def stream_gemini_response(api_key: str, user_message: str, image_path: Optional[str] = None) -> Generator[str, None, None]:
    """
    Get response from the Gemini API using google-generativeai library.
    
    Args:
        api_key (str): The Gemini API key
        user_message (str): The user's input message
        image_path (Optional[str]): Path to the image file, if any
        
    Yields:
        str: The generated response
    """
    try:
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        # Create a GenerativeModel instance - use Pro model for image inputs
        model = genai.GenerativeModel("gemini-1.5-pro")
        
        # Set up generation config
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 2048,
        }
        
        logger.info("Sending request to Gemini API...")
        
        # Generate the response
        if image_path:
            try:
                # Open and prepare the image
                image = Image.open(image_path)
                response = model.generate_content(
                    [user_message, image],
                    generation_config=generation_config
                )
            except Exception as e:
                logger.error(f"Error processing image: {str(e)}")
                yield "Sorry, I couldn't process the image. Please make sure it's a valid image file."
                return
        else:
            # Text-only model for regular queries
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(
                user_message,
                generation_config=generation_config
            )
        
        if response.text:
            yield response.text
        else:
            yield "Sorry, I couldn't generate a meaningful response."
            
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        yield f"An error occurred while processing your request: {str(e)}"
