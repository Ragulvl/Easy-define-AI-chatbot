"""
AI Chatbot Application with GUI
Main application file using Tkinter for the user interface.
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
from gemini_helper import initialize_gemini, get_chat_response


class ChatbotApp:
    """
    Main application class for the AI Chatbot.
    """
    
    def __init__(self, root):
        """
        Initialize the chatbot application.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("AI Chatbot - Gemini")
        self.root.geometry("600x700")
        self.root.resizable(True, True)
        
        # API key - Replace with your own key or load from environment variable
        self.api_key = "AIzaSyBJdKWXME2lCZjYMMZSx0oH3qLkBHEN0ME"
        
        # Initialize the Gemini model
        self.model = None
        try:
            self.model = initialize_gemini(self.api_key)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize Gemini API:\n{str(e)}")
            return
        
        # Chat history to maintain conversation context
        self.chat_history = []
        
        # Create the GUI components
        self.create_widgets()
        
    def create_widgets(self):
        """
        Create and arrange all GUI components.
        """
        # Chat display area (scrollable text widget)
        # This shows the conversation history
        self.chat_display = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            width=70,
            height=30,
            state=tk.DISABLED,  # Disabled to prevent direct editing
            font=("Arial", 10)
        )
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Welcome message
        self.add_message_to_chat("Bot", "Hello! I'm your AI assistant. How can I help you today?")
        
        # Frame for input area (contains input box and send button)
        input_frame = tk.Frame(self.root)
        input_frame.pack(padx=10, pady=10, fill=tk.X)
        
        # Text input box for user messages
        self.user_input = tk.Entry(
            input_frame,
            font=("Arial", 11),
            width=50
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Bind Enter key to send message
        self.user_input.bind("<Return>", lambda event: self.send_message())
        
        # Send button
        send_button = tk.Button(
            input_frame,
            text="Send",
            command=self.send_message,
            font=("Arial", 11),
            bg="#4CAF50",
            fg="white",
            padx=20,
            cursor="hand2"
        )
        send_button.pack(side=tk.RIGHT)
        
        # Focus on the input box when the app starts
        self.user_input.focus()
        
    def add_message_to_chat(self, sender, message):
        """
        Add a message to the chat display area.
        
        Args:
            sender (str): Either "User" or "Bot"
            message (str): The message content
        """
        # Enable the text widget to allow editing
        self.chat_display.config(state=tk.NORMAL)
        
        # Format the message with sender label
        formatted_message = f"{sender}: {message}\n\n"
        
        # Insert the message at the end
        self.chat_display.insert(tk.END, formatted_message)
        
        # Disable the text widget again to prevent editing
        self.chat_display.config(state=tk.DISABLED)
        
        # Auto-scroll to the bottom to show the latest message
        self.chat_display.see(tk.END)
        
    def send_message(self):
        """
        Handle sending a message when the user clicks Send or presses Enter.
        """
        # Get the user's message from the input box
        user_message = self.user_input.get().strip()
        
        # Don't send empty messages
        if not user_message:
            return
        
        # Clear the input box
        self.user_input.delete(0, tk.END)
        
        # Display the user's message in the chat
        self.add_message_to_chat("User", user_message)
        
        # Show "Bot is typing..." message
        self.add_message_to_chat("Bot", "Thinking...")
        
        # Update the window to show the "Thinking..." message
        self.root.update()
        
        # Get response from Gemini API
        if self.model:
            try:
                # Get bot response
                bot_response = get_chat_response(self.model, user_message, self.chat_history)
                
                # Remove the "Thinking..." message
                self.chat_display.config(state=tk.NORMAL)
                self.chat_display.delete("end-2l", "end-1l")  # Remove last line
                self.chat_display.config(state=tk.DISABLED)
                
                # Display the actual bot response
                self.add_message_to_chat("Bot", bot_response)
                
                # Update chat history for context (optional, for future use)
                self.chat_history.append(f"User: {user_message}")
                self.chat_history.append(f"Bot: {bot_response}")
                
                # Keep only last 10 exchanges to avoid token limits
                if len(self.chat_history) > 20:
                    self.chat_history = self.chat_history[-20:]
                    
            except Exception as e:
                # Remove the "Thinking..." message
                self.chat_display.config(state=tk.NORMAL)
                self.chat_display.delete("end-2l", "end-1l")
                self.chat_display.config(state=tk.DISABLED)
                
                # Show error message
                error_msg = f"Error: {str(e)}"
                self.add_message_to_chat("Bot", error_msg)
        else:
            # Remove the "Thinking..." message
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete("end-2l", "end-1l")
            self.chat_display.config(state=tk.DISABLED)
            
            # Show error if model is not initialized
            self.add_message_to_chat("Bot", "Error: AI model not initialized. Please check your API key.")


def main():
    """
    Main function to start the application.
    """
    # Create the main window
    root = tk.Tk()
    
    # Create and run the application
    app = ChatbotApp(root)
    
    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    main()

