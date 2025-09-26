# apps/core/management/commands/seed_data.py

import random
import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from faker import Faker

from apps.users.models import CustomUser
from apps.learning.models import Course, Lesson, LearningPath, LearningPathCourse
from apps.enrollment.models import Enrollment, CompletedLesson
from apps.contracts.models import Contract
from apps.enrollment.services import calculate_progress

class Command(BaseCommand):
    help = 'Seeds the database with a large amount of rich and diverse dummy data.'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        if CustomUser.objects.count() > 10:
            self.stdout.write(self.style.WARNING('Database already contains data. Seeding skipped.'))
            return

        self.stdout.write(self.style.SUCCESS('🚀 Starting comprehensive database seeding...'))
        fake = Faker()

        # -- 1. Create Users --
        self.stdout.write('👤 Creating users...')
        supervisors = [
            CustomUser.objects.create_user(
                username=f'supervisor{i}', email=f'supervisor{i}@example.com', password='password',
                role=CustomUser.Roles.SUPERVISOR, full_name=fake.name()
            ) for i in range(5)
        ]
        instructors = [
            CustomUser.objects.create_user(
                username=f'instructor{i}', email=f'instructor{i}@example.com', password='password',
                role=CustomUser.Roles.INSTRUCTOR, full_name=fake.name()
            ) for i in range(25)
        ]
        b2b_clients = [
            CustomUser.objects.create_user(
                username=fake.company().lower().replace(' ', ''), email=f'client{i}@company.com', password='password',
                role=CustomUser.Roles.THIRD_PARTY, full_name=f'{fake.company()} Client'
            ) for i in range(20)
        ]
        students = [
            CustomUser.objects.create_user(
                username=f'student{i}', email=f'student{i}@example.com', password='password',
                role=CustomUser.Roles.STUDENT, full_name=fake.name()
            ) for i in range(1800)
        ]

        # -- 2. Create Courses and Lessons --
        self.stdout.write('📚 Creating courses and lessons...')
        courses = []
        course_categories = ['Data Science', 'Web Development', 'Digital Marketing', 'Business Management', 'UI/UX Design', 'Cloud Computing']
        for i in range(100):
            course = Course.objects.create(
                title=f'{random.choice(["Mastering", "Advanced", "Introduction to"])} {fake.job()}',
                slug=f'course-{fake.slug()}-{i}',
                description=fake.paragraph(nb_sentences=10),
                instructor=random.choice(instructors),
                category=random.choice(course_categories),
                status=Course.CourseStatus.PUBLISHED
            )
            courses.append(course)
            for j in range(random.randint(15, 30)):
                Lesson.objects.create(
                    course=course, title=f'Module {j+1}: {fake.sentence(nb_words=5)}', order=j,
                    content_type=random.choice([Lesson.ContentType.VIDEO, Lesson.ContentType.TEXT, Lesson.ContentType.PDF]),
                    content_data={'url': fake.url(), 'duration_minutes': random.randint(5, 25)}
                )

        # -- 3. Create Learning Paths --
        self.stdout.write('🛤️ Creating learning paths...')
        for i in range(20):
            path = LearningPath.objects.create(
                title=f'Professional Certificate in {random.choice(course_categories)}',
                description=fake.paragraph(nb_sentences=5),
                supervisor=random.choice(supervisors)
            )
            path_courses = random.sample(courses, k=random.randint(4, 8))
            for order, course in enumerate(path_courses):
                LearningPathCourse.objects.create(learning_path=path, course=course, order=order)

        # -- 4. Create B2B Contracts --
        self.stdout.write('💼 Creating B2B contracts...')
        for client in b2b_clients:
            contract_students = random.sample(students, k=random.randint(10, 50))
            contract = Contract.objects.create(
                title=f'Training Contract for {client.full_name}',
                client=client,
                start_date=timezone.now() - datetime.timedelta(days=random.randint(30, 90)),
                end_date=timezone.now() + datetime.timedelta(days=365)
            )
            contract.enrolled_students.set(contract_students)

        # -- 5. Create Enrollments and Simulate Progress --
        self.stdout.write('📈 Creating enrollments and simulating progress...')
        for student in random.sample(students, k=1500): # Enroll most students
            courses_to_enroll = random.sample(courses, k=random.randint(1, 5))
            for course in courses_to_enroll:
                enrollment = Enrollment.objects.create(student=student, course=course)
                
                # Simulate progress for some enrollments
                if random.random() > 0.3: # 70% chance to have some progress
                    lessons_in_course = list(course.lessons.all())
                    if lessons_in_course:
                        # Complete a random percentage of lessons
                        completed_count = int(len(lessons_in_course) * random.uniform(0.1, 0.95))
                        lessons_to_complete = random.sample(lessons_in_course, k=completed_count)
                        
                        for lesson in lessons_to_complete:
                            CompletedLesson.objects.create(enrollment=enrollment, lesson=lesson)
                        
                        # Update progress percentage
                        calculate_progress(enrollment.id)

        self.stdout.write(self.style.SUCCESS('✅ Database has been seeded with rich, diverse data!'))