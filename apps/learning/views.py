"""
Views for the 'learning' application.

This module contains views for displaying and managing learning content, such as
viewing a lesson, managing a course's structure, and building learning paths.
Many views are designed to be driven by HTMX for a dynamic user experience.
"""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, CreateView, UpdateView
from django.views import View

from .models import Course, Workshop, Lesson, LearningPath
from .forms import CourseForm, WorkshopForm, LearningPathForm, LessonForm


class InstructorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin to ensure the user has the 'instructor' or 'admin' role.
    """
    def test_func(self):
        return self.request.user.role in [self.request.user.Roles.INSTRUCTOR, self.request.user.Roles.ADMIN]


class LessonDetailView(LoginRequiredMixin, DetailView):
    """
    Displays the content of a single lesson.

    This is the primary view for students to consume learning material. It fetches
    the lesson and its course/workshop to provide context and navigation.
    """
    model = Lesson
    template_name = "learning/lesson_detail.html"
    context_object_name = "lesson"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = self.get_object()
        # Set the parent content object (course or workshop)
        context["content_object"] = lesson.course or lesson.workshop
        return context


class CourseManageView(InstructorRequiredMixin, DetailView):
    """
    Provides an interface for instructors to manage a course's content.
    """
    model = Course
    template_name = "learning/manage_course.html"
    context_object_name = "course"


class WorkshopManageView(InstructorRequiredMixin, DetailView):
    """
    Provides an interface for instructors to manage a workshop's content.
    """
    model = Workshop
    template_name = "learning/manage_workshop.html"
    context_object_name = "workshop"


class PathBuilderView(LoginRequiredMixin, DetailView):
    """
    A drag-and-drop interface for supervisors to build Learning Paths.
    """
    model = LearningPath
    template_name = "learning/path_builder.html"
    context_object_name = "learning_path"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["available_courses"] = Course.objects.filter(status=Course.CourseStatus.PUBLISHED)
        return context


class LearningPathCreateView(LoginRequiredMixin, FormView):
    """
    View for creating a new Learning Path.
    """
    template_name = 'learning/path_form.html'
    form_class = LearningPathForm
    success_url = reverse_lazy("core:dashboard") # Placeholder

    def form_valid(self, form):
        self.object = form.save()
        # In a real app, success_url would redirect to the path_builder view.
        # success_url = reverse_lazy('learning:path-builder', kwargs={'pk': self.object.pk})
        return super().form_valid(form)


class QuizTakeView(LoginRequiredMixin, DetailView):
    """
    View for a student to take a quiz.
    """
    model = Lesson
    template_name = "learning/take_quiz.html"
    context_object_name = "lesson"


class QuizResultView(LoginRequiredMixin, View):
    """
    View to display the results of a quiz attempt.
    """
    def get(self, request, attempt_id, *args, **kwargs):
        # attempt = get_object_or_404(QuizAttempt, id=attempt_id)
        return render(request, "learning/quiz_result.html", {"attempt_id": attempt_id})