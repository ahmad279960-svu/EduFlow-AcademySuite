"""
Custom template tags and filters for the 'interactions' application.
"""
from django import template
from apps.interactions.forms import DiscussionThreadForm, DiscussionPostForm

register = template.Library()


@register.inclusion_tag('interactions/partials/_thread_form.html')
def render_thread_form(lesson):
    """
    Renders the form for creating a new discussion thread.

    :param lesson: The lesson object to associate the form with.
    :type lesson: apps.learning.models.Lesson
    :returns: A dictionary with the form and lesson.
    :rtype: dict
    """
    form = DiscussionThreadForm()
    return {'form': form, 'lesson': lesson}


@register.inclusion_tag('interactions/partials/_post_form.html')
def render_post_form(thread):
    """
    Renders the form for creating a new post (reply) in a thread.

    :param thread: The thread object to associate the form with.
    :type thread: apps.interactions.models.DiscussionThread
    :returns: A dictionary with the form and thread.
    :rtype: dict
    """
    form = DiscussionPostForm()
    return {'form': form, 'thread': thread}