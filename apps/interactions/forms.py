"""
Django Forms for the 'interactions' application.

This module provides forms for creating discussion threads and posts, which will
be used in the HTMX-driven frontend views.
"""
from django import forms
from .models import DiscussionThread, DiscussionPost


class DiscussionThreadForm(forms.ModelForm):
    """
    Form for creating a new discussion thread (a question).
    """
    class Meta:
        model = DiscussionThread
        fields = ['title', 'question']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter question title'}),
            'question': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe your question in detail...'}),
        }


class DiscussionPostForm(forms.ModelForm):
    """
    Form for creating a new discussion post (a reply).
    """
    class Meta:
        model = DiscussionPost
        fields = ['reply_text']
        labels = {
            'reply_text': '',  # Hide the label as it's often intuitive
        }
        widgets = {
            'reply_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write a reply...'}),
        }