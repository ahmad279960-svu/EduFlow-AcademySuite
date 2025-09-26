"""
Business logic services for the 'interactions' application.

This module contains the service layer for complex interactions, most notably
the integration with the external AI Assistant service (OpenRouter).
"""
import requests
from django.conf import settings


class AIAssistantService:
    """
    A service class to handle all interactions with the AI assistant provider.

    This encapsulates the logic for building the prompt, making the API call,
    and handling the response, decoupling the rest of the application from the
    specifics of the AI provider's API.
    """

    def __init__(self, model: str = "openai/gpt-3.5-turbo"):
        """
        Initializes the service with API credentials and settings.

        :param model: The specific model to use via OpenRouter.
        :type model: str
        """
        self.api_key = getattr(settings, "OPENROUTER_API_KEY", None)
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.site_name = "EduFlow Academy"
        self.model = model

    def get_ai_response(self, question: str, context: dict) -> str:
        """
        Gets a response from the AI assistant for a given question and context.

        :param question: The user's question.
        :type question: str
        :param context: A dictionary containing contextual info like course/lesson title.
        :type context: dict
        :returns: The AI's response text, or an error message.
        :rtype: str
        """
        if not self.api_key:
            return "AI Assistant is not configured. Missing API key."

        prompt = self._build_prompt(question, context)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()  # Raise an exception for bad status codes
            response_data = response.json()
            return response_data["choices"][0]["message"]["content"]
        except requests.RequestException as e:
            # Log the exception `e` in a real application
            return "Sorry, there was an error communicating with the AI Assistant."
        except (KeyError, IndexError):
            # Handle unexpected response format
            return "Sorry, the AI Assistant returned an unexpected response."

    def _build_prompt(self, question: str, context: dict) -> str:
        """
        Constructs a detailed prompt for the large language model.

        :param question: The user's question.
        :type question: str
        :param context: A dictionary containing contextual info.
        :type context: dict
        :returns: The fully constructed prompt string.
        :rtype: str
        """
        course_title = context.get("course_title", "the course")
        lesson_title = context.get("lesson_title", "the current lesson")

        prompt = (
            f"You are a helpful teaching assistant for an online learning platform called '{self.site_name}'.\n"
            f"A student is currently in the course '{course_title}' and on the lesson '{lesson_title}'.\n"
            f"The student's question is: '{question}'\n\n"
            f"Please provide a clear, concise, and helpful answer to the student's question in the context of this lesson. "
            f"Do not invent information if you don't know the answer. Be encouraging and supportive."
        )
        return prompt