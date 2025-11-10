"""
Gemini API Helper Module
This module handles all interactions with the Google Gemini API.
"""

import google.generativeai as genai


def initialize_gemini(api_key):
    """
    Initialize the Gemini API with the provided API key.
    
    Args:
        api_key (str): Your Google Gemini API key
        
    Returns:
        model: Configured Gemini model instance
    """
    try:
        # Configure the API with the provided key
        genai.configure(api_key=api_key)
        
        # Create and return a model instance
        # Using 'gemini-pro' model (you can change this to other available models)
        model = genai.GenerativeModel('gemini-pro')
        return model
    except Exception as e:
        raise Exception(f"Failed to initialize Gemini API: {str(e)}")


def get_chat_response(model, user_message, chat_history=None):
    """
    Get a response from the Gemini API based on user's message.
    
    Args:
        model: The initialized Gemini model
        user_message (str): The message from the user
        chat_history (list, optional): Previous conversation history
        
    Returns:
        str: The bot's response
    """
    try:
        # If there's chat history, include it in the context
        if chat_history:
            # Format the chat history for the API
            full_prompt = "\n".join(chat_history) + f"\nUser: {user_message}\nBot:"
        else:
            # For the first message, just use the user's message
            full_prompt = user_message
        
        # Generate response from the model
        response = model.generate_content(full_prompt)
        
        # Extract and return the text response
        return response.text.strip()
    except Exception as e:
        # Return a user-friendly error message
        return f"Error: Unable to get response from AI. {str(e)}"

