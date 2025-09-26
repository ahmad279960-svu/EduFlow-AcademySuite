"""
Views for the 'interactions' application.

This module contains the views that handle the frontend logic for the discussion
forum and other interactive features. These views are designed to respond to
HTMX requests, returning HTML fragments to create a dynamic user experience.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, DetailView
from django.views import View

from .models import DiscussionThread, DiscussionPost
from .forms import DiscussionThreadForm, DiscussionPostForm
from apps.learning.models import Lesson


class AddDiscussionThreadView(LoginRequiredMixin, CreateView):
    """
    Handles the creation of a new discussion thread via HTMX.
    """
    model = DiscussionThread
    form_class = DiscussionThreadForm
    template_name = "interactions/partials/_discussion_list.html" # Rerender the list on success

    def form_valid(self, form):
        """
        Processes a valid form submission.
        """
        lesson = get_object_or_404(Lesson, pk=self.kwargs['lesson_pk'])
        form.instance.lesson = lesson
        form.instance.student = self.request.user
        form.save()
        
        # After saving, render the updated list of threads for the lesson
        threads = DiscussionThread.objects.filter(lesson=lesson)
        return render(self.request, self.template_name, {'threads': threads, 'lesson': lesson})


class AddDiscussionPostView(LoginRequiredMixin, CreateView):
    """
    Handles the creation of a new discussion post (reply) via HTMX.
    """
    model = DiscussionPost
    form_class = DiscussionPostForm
    template_name = "interactions/partials/_thread_detail.html" # Rerender the thread on success

    def form_valid(self, form):
        """
        Processes a valid form submission.
        """
        thread = get_object_or_404(DiscussionThread, pk=self.kwargs['thread_pk'])
        form.instance.thread = thread
        form.instance.user = self.request.user
        form.save()

        # After saving, render the updated thread detail view
        return render(self.request, self.template_name, {'thread': thread})


class ThreadDetailView(LoginRequiredMixin, DetailView):
    """
    Displays the details of a single discussion thread, including all its posts.
    """
    model = DiscussionThread
    template_name = "interactions/partials/_thread_detail.html"
    context_object_name = "thread"


class AIChatFormView(LoginRequiredMixin, View):
    """
    A simple view that renders the AI chat form component.
    """
    def get(self, request, *args, **kwargs):
        """
        Renders the AI chat form partial.
        """
        lesson = get_object_or_404(Lesson, pk=kwargs.get('lesson_pk'))
        return render(request, "interactions/partials/_ai_chat_form.html", {"lesson": lesson})