"""
Django Forms for the 'learning' application.

This module provides forms for creating and editing core learning objects like
Courses and Learning Paths, to be used in the application's frontend views.
"""
from django import forms
from .models import Course, LearningPath, Lesson
from apps.users.models import CustomUser


class CourseForm(forms.ModelForm):
    """
    Form for creating and updating a Course.
    """
    class Meta:
        model = Course
        fields = [
            "title",
            "slug",
            "description",
            "instructor",
            "category",
            "status",
            "cover_image_url",
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter the instructor dropdown to only show users with the 'instructor' role.
        self.fields['instructor'].queryset = CustomUser.objects.filter(
            role=CustomUser.Roles.INSTRUCTOR
        )


class LearningPathForm(forms.ModelForm):
    """
    Form for creating and updating a Learning Path.
    """
    class Meta:
        model = LearningPath
        fields = ["title", "description", "supervisor"]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter the supervisor dropdown to only show users with the 'supervisor' role.
        self.fields['supervisor'].queryset = CustomUser.objects.filter(
            role=CustomUser.Roles.SUPERVISOR
        )


class LessonForm(forms.ModelForm):
    """
    Form for creating and updating a Lesson.
    """
    class Meta:
        model = Lesson
        fields = ["title", "content_type"]