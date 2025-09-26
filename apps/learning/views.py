"""
Views for the 'learning' application.

This module contains views for displaying and managing learning content, such as
viewing a lesson, managing a course's structure, and building learning paths.
Many views are designed to be driven by HTMX for a dynamic user experience.
"""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, CreateView
from django.views import View

from .models import Course, Workshop, Lesson, LearningPath
from .forms import CourseForm, WorkshopForm, LearningPathForm, LessonForm
from apps.users.models import CustomUser
from apps.enrollment.models import Enrollment, LessonProgress


class InstructorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin to ensure the user has the 'instructor' or 'admin' role.
    """
    def test_func(self):
        return self.request.user.role in [CustomUser.Roles.INSTRUCTOR, CustomUser.Roles.ADMIN]


class SupervisorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin to ensure the user has the 'supervisor' or 'admin' role.
    """
    def test_func(self):
        return self.request.user.role in [CustomUser.Roles.SUPERVISOR, CustomUser.Roles.ADMIN]


# --- Content Creation & Management Views ---

class CourseCreateView(InstructorRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = "learning/partials/_course_form.html"

    def form_valid(self, form):
        form.instance.instructor = self.request.user
        form.save()
        response = HttpResponse(status=204)
        response["HX-Trigger"] = "contentListChanged"
        return response


class WorkshopCreateView(InstructorRequiredMixin, CreateView):
    model = Workshop
    form_class = WorkshopForm
    template_name = "learning/partials/_workshop_form.html"

    def form_valid(self, form):
        form.instance.instructor = self.request.user
        form.save()
        response = HttpResponse(status=204)
        response["HX-Trigger"] = "contentListChanged"
        return response


class LearningPathCreateView(SupervisorRequiredMixin, CreateView):
    model = LearningPath
    form_class = LearningPathForm
    template_name = "learning/partials/_path_form.html"
    
    def form_valid(self, form):
        form.instance.supervisor = self.request.user
        form.save()
        response = HttpResponse(status=204)
        response["HX-Trigger"] = "pathListChanged"
        return response


class LessonCreateView(InstructorRequiredMixin, CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = "learning/partials/_lesson_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_pk'] = self.kwargs.get('course_pk')
        context['workshop_pk'] = self.kwargs.get('workshop_pk')
        return context

    def form_valid(self, form):
        course_pk = self.kwargs.get('course_pk')
        workshop_pk = self.kwargs.get('workshop_pk')
        
        if course_pk:
            form.instance.course = get_object_or_404(Course, pk=course_pk)
        elif workshop_pk:
            form.instance.workshop = get_object_or_404(Workshop, pk=workshop_pk)
        
        form.save()
        response = HttpResponse(status=204)
        response["HX-Trigger"] = "lessonListChanged"
        return response

# --- Student Progress & Monitoring Views ---

class CourseStudentProgressView(InstructorRequiredMixin, DetailView):
    model = Course
    template_name = "learning/course_student_progress.html"
    context_object_name = "course"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        enrollments = Enrollment.objects.filter(course=course) \
            .select_related('student') \
            .order_by('student__full_name')
        context['enrollments'] = enrollments
        return context


class StudentDetailProgressView(InstructorRequiredMixin, DetailView):
    model = Enrollment
    template_name = "learning/student_detail_progress.html"
    context_object_name = "enrollment"

    def get_queryset(self):
        return super().get_queryset().select_related('student', 'course').prefetch_related('lesson_progress__lesson')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        enrollment = self.get_object()
        
        progress_map = {lp.lesson.pk: lp for lp in enrollment.lesson_progress.all()}
        
        all_lessons = enrollment.course.lessons.all().order_by('order')
        lesson_progress_list = []
        for lesson in all_lessons:
            progress_obj, _ = LessonProgress.objects.get_or_create(enrollment=enrollment, lesson=lesson)
            lesson_progress_list.append(progress_obj)

        context['lesson_progress_list'] = lesson_progress_list
        return context


class WorkshopAttendanceView(InstructorRequiredMixin, DetailView):
    """
    Displays an attendance sheet for a specific workshop session (lesson).
    """
    model = Lesson
    template_name = "learning/workshop_attendance.html"
    context_object_name = "lesson"

    def get_queryset(self):
        return super().get_queryset().select_related('workshop')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = self.get_object()
        workshop = lesson.workshop
        
        # Find students enrolled in this workshop via contracts
        # This is a simplified logic; a more robust solution might involve direct workshop enrollment
        contracts = workshop.contracts.prefetch_related('enrolled_students')
        students = CustomUser.objects.filter(
            contracts_enrolled_in__in=contracts
        ).distinct().order_by('full_name')
        
        context['students'] = students
        return context

# --- Main Page Views ---

class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = "learning/lesson_detail.html"
    context_object_name = "lesson"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = self.get_object()
        context["content_object"] = lesson.course or lesson.workshop
        return context


class CourseManageView(InstructorRequiredMixin, DetailView):
    model = Course
    template_name = "learning/manage_course.html"
    context_object_name = "course"


class WorkshopManageView(InstructorRequiredMixin, DetailView):
    model = Workshop
    template_name = "learning/manage_workshop.html"
    context_object_name = "workshop"


class PathBuilderView(SupervisorRequiredMixin, DetailView):
    model = LearningPath
    template_name = "learning/path_builder.html"
    context_object_name = "learning_path"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["available_courses"] = Course.objects.filter(status=Course.CourseStatus.PUBLISHED)
        return context

# --- Quiz Views ---

class QuizTakeView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = "learning/take_quiz.html"
    context_object_name = "lesson"


class QuizResultView(LoginRequiredMixin, View):
    def get(self, request, attempt_id, *args, **kwargs):
        return render(request, "learning/quiz_result.html", {"attempt_id": attempt_id})