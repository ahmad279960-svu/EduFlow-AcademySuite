"""
Views for the 'learning' application.

This module contains views for displaying and managing learning content, such as
viewing a lesson, managing a course's structure, and building learning paths.
Many views are designed to be driven by HTMX for a dynamic user experience.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, FormView
from django.views import View
from .models import Course, Lesson, LearningPath
from .forms import LearningPathForm


class LessonDetailView(LoginRequiredMixin, DetailView):
    """
    Displays the content of a single lesson.

    This is the primary view for students to consume learning material. It fetches
    the lesson and its course to provide context and navigation.
    """
    model = Lesson
    template_name = "learning/lesson_detail.html"
    context_object_name = "lesson"

    def get_context_data(self, **kwargs):
        """
        Adds related data to the template context.
        """
        context = super().get_context_data(**kwargs)
        lesson = self.get_object()
        context["course"] = lesson.course
        # In a real scenario, we'd also pass enrollment progress here.
        return context


class CourseManageView(LoginRequiredMixin, DetailView):
    """
    Provides an interface for instructors to manage a course's content.

    This view displays the structure of a course (its lessons) and allows for
    actions like adding, editing, and reordering lessons, primarily via HTMX.
    """
    model = Course
    template_name = "learning/manage_course.html"
    context_object_name = "course"
    # Add permission checks here in a real application, e.g., user must be instructor.


class PathBuilderView(LoginRequiredMixin, DetailView):
    """
    A drag-and-drop interface for supervisors to build Learning Paths.

    This view displays a learning path and a list of available courses. The user
    can drag courses into the path and reorder them. The saving logic is handled
    by a dedicated API endpoint called by HTMX/JavaScript.
    """
    model = LearningPath
    template_name = "learning/path_builder.html"
    context_object_name = "learning_path"
    # Add permission checks here in a real application.

    def get_context_data(self, **kwargs):
        """
        Adds the list of all available courses to the context.
        """
        context = super().get_context_data(**kwargs)
        context["available_courses"] = Course.objects.filter(status=Course.CourseStatus.PUBLISHED)
        return context


class LearningPathCreateView(LoginRequiredMixin, FormView):
    """
    View for creating a new Learning Path.
    """
    template_name = 'learning/path_form.html'
    form_class = LearningPathForm
    # In a real app, success_url would redirect to the path_builder view.
    # success_url = reverse_lazy('learning:path-builder', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        # Logic to save the form and redirect
        self.object = form.save()
        # You would implement the redirect logic here.
        return super().form_valid(form)


class QuizTakeView(LoginRequiredMixin, DetailView):
    """
    View for a student to take a quiz.
    """
    model = Lesson
    template_name = "learning/take_quiz.html"
    context_object_name = "lesson"
    # Add permission checks to ensure the lesson is a quiz type.


class QuizResultView(LoginRequiredMixin, View):
    """
    View to display the results of a quiz attempt.
    This view will receive the attempt ID and display the score.
    """
    def get(self, request, attempt_id, *args, **kwargs):
        # In a real implementation, you'd fetch the QuizAttempt object
        # from the 'enrollment' app using the attempt_id.
        # For now, this is a placeholder.
        # attempt = get_object_or_404(QuizAttempt, id=attempt_id)
        return render(request, "learning/quiz_result.html", {"attempt_id": attempt_id})