"""
Custom template tags and filters for the 'learning' application, specifically
for functionality related to quizzes.
"""
from django import template

register = template.Library()

# Example filter - can be expanded later
@register.filter(name="get_user_answer")
def get_user_answer(question, attempt):
    """
    A template filter to retrieve the user's selected answer for a given question
    within a specific quiz attempt.

    Usage: {{ question|get_user_answer:quiz_attempt }}

    :param question: The question object.
    :type question: apps.learning.models.Question
    :param attempt: The quiz attempt object.
    :type attempt: apps.enrollment.models.QuizAttempt
    :returns: The user's QuizAnswer object for that question, or None.
    :rtype: apps.enrollment.models.QuizAnswer or None
    """
    # This relies on the 'enrollment' app's models.
    # It demonstrates the cross-app relationship.
    try:
        # The related_name on QuizAttempt's foreign key to Question is 'user_answers'
        return attempt.user_answers.get(question=question)
    except:
        return None