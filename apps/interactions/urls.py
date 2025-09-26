"""
URL configuration for the 'interactions' application.

Defines the URL patterns for creating and viewing discussion threads and posts,
designed to be called from the frontend via HTMX.
"""
from django.urls import path
from . import views

app_name = "interactions"

urlpatterns = [
    path("thread/add/<uuid:lesson_pk>/", views.AddDiscussionThreadView.as_view(), name="thread-add"),
    path("thread/<uuid:pk>/", views.ThreadDetailView.as_view(), name="thread-detail"),
    path("post/add/<uuid:thread_pk>/", views.AddDiscussionPostView.as_view(), name="post-add"),
    path("ai-chat-form/<uuid:lesson_pk>/", views.AIChatFormView.as_view(), name="ai-chat-form"),
]