# Import necessary libraries and modules
import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List
import webbrowser

# Load your OpenAI API key
# models.OpenAI.api_key = "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"
# or from environment variable:
models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with a mental health support bot named Dr. GPT. I'm here to provide a listening ear and offer guidance on mental well-being. Remember, I am not a licensed therapist or counselor. If you need immediate help, please call emergency services or a helpline in your country.

How can I support you today, [USER_NAME]? Feel free to share your thoughts or concerns with me.
"""

MENTAL_HEALTH_KEYWORDS = ["anxious", "depressed", "stressed", "lonely", "suicidal", 'sad']

MENTAL_HEALTH_RESPONSE = """I'm really sorry to hear that you're feeling this way. It's important to remember that you don't have to face this alone. Reach out for support from friends, family, or a professional. In the meantime, you may find it helpful to visit [MENTAL_HEALTH_RESOURCE_LINK] for more information on coping strategies. Is there anything specific you'd like to discuss or any support I can offer right now?"""

MENTAL_HEALTH_RESOURCE_LINK = "https://www.mentalhealthadviser.co.uk/"

# Function to check if the response is safe
def check_response(response):
    # Add your moderation checks here
    # For this example, we'll use a simple keyword-based check to detect harmful content
    harmful_keywords = ["harm", "suicide", "dangerous"]
    return not any(keyword in response.lower() for keyword in harmful_keywords)

# Function to get a safe default response
def get_safe_default_response():
    return "I apologize, but I can't provide a response at the moment. Please seek support from a mental health professional or a trusted person in your life."

@textbase.chatbot("mental-health-support-bot")
def on_message(message_history: List[Message], state: dict = None):
    if state is None or "counter" not in state:
        state = {"counter": 0}
    else:
        state["counter"] += 1

    # Extract user input from the last message
    last_user_message = message_history[-1].content.strip()

    last_keyword = last_user_message.split()[-1]

    # Check if the user's message contains mental health-related keywords
    is_mental_health_prompt = any(keyword in last_user_message for keyword in MENTAL_HEALTH_KEYWORDS)


    

    if is_mental_health_prompt:
        # Ask guided questions for certain mental health keywords
        bot_response = f"I'm sorry to hear that you're feeling {last_keyword}. Can you tell me more about what's been bothering you? or else you can visit at {MENTAL_HEALTH_RESOURCE_LINK} for mental health advice and information . "
    else:
        # Generate GPT-3.5 Turbo response
        user_name = "User"  # You can get the user's name from the platform if available
        system_prompt = SYSTEM_PROMPT.replace("[USER_NAME]", user_name)
        bot_response = models.OpenAI.generate(
            system_prompt=system_prompt + "\n" + last_user_message,
            message_history=message_history,
            model="gpt-3.5-turbo",
        )

    # Check the generated response using the moderation system
    if not check_response(bot_response):
        bot_response = get_safe_default_response()

    # Return the response and updated state
    return bot_response, state
