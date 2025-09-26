"""
Management command to seed the database with rich and diverse dummy data.

This command populates the database with a complete set of interconnected objects,
including users, courses, workshops, learning paths, contracts, and enrollments,
to provide a realistic environment for testing and demonstration.
"""
import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from faker import Faker
from tqdm import tqdm

from apps.users.models import CustomUser
from apps.learning.models import Course, Workshop, Lesson, LearningPath, LearningPathCourse
from apps.enrollment.models import Enrollment, LessonProgress
from apps.contracts.models import Contract
from apps.enrollment.services import calculate_progress

class Command(BaseCommand):
    help = 'Seeds the database with a large, interconnected set of dummy data.'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        if CustomUser.objects.count() > 1:
            self.stdout.write(self.style.WARNING('Database appears to be already seeded. Aborting command.'))
            return

        self.stdout.write(self.style.SUCCESS('🚀 Starting comprehensive database seeding...'))
        fake = Faker()

        # -- 1. Create Users --
        self.stdout.write('👤 Creating users...')

        # Check if the superuser from the previous step exists, if not, create one.
        if not CustomUser.objects.filter(username='admin').exists():
            CustomUser.objects.create_superuser('admin', 'admin@example.com', 'password', role=CustomUser.Roles.ADMIN, full_name='Platform Admin')

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
            ) for i in range(20)
        ]
        students = [
            CustomUser.objects.create_user(
                username=f'student{i}', email=f'student{i}@example.com', password='password',
                role=CustomUser.Roles.STUDENT, full_name=fake.name()
            ) for i in tqdm(range(500), 'Creating students')
        ]

        # Ensure unique company names for usernames
        b2b_clients = []
        for i in range(10):
            company_name = fake.unique.company().lower().replace(' ', '').replace(',', '')
            b2b_clients.append(
                CustomUser.objects.create_user(
                    username=company_name, email=f'client{i}@company.com', password='password',
                    role=CustomUser.Roles.THIRD_PARTY, full_name=f'{fake.company()} Client'
                )
            )

        # -- 2. Create Courses, Workshops, and Lessons --
        self.stdout.write('📚 Creating courses, workshops, and lessons...')
        courses = []
        course_categories = ['Data Science', 'Web Development', 'Digital Marketing', 'Business', 'Design', 'Cloud Computing']
        for i in tqdm(range(50), 'Creating Courses'):
            course = Course.objects.create(
                title=f'{random.choice(["Mastering", "Advanced", "Intro to"])} {random.choice(course_categories)}',
                slug=f'course-{fake.unique.slug()}-{i}',
                description=fake.paragraph(nb_sentences=8),
                instructor=random.choice(instructors),
                category=random.choice(course_categories),
                status=Course.CourseStatus.PUBLISHED
            )
            courses.append(course)
            for j in range(random.randint(10, 25)):
                Lesson.objects.create(
                    course=course, title=f'Module {j+1}: {fake.sentence(nb_words=4)}', order=j,
                    content_type=random.choice([Lesson.ContentType.VIDEO, Lesson.ContentType.TEXT, Lesson.ContentType.PDF]),
                    content_data={'url': fake.url()}
                )

        workshop_content_types = [choice[0] for choice in Lesson.ContentType.choices if choice[0] != 'quiz']
        for i in tqdm(range(15), 'Creating Workshops'):
            workshop = Workshop.objects.create(
                title=f'{fake.job()} Workshop',
                description=fake.paragraph(nb_sentences=6),
                instructor=random.choice(instructors),
                workshop_type=random.choice([wt[0] for wt in Workshop.WorkshopType.choices]),
                category=random.choice([wc[0] for wc in Workshop.WorkshopCategory.choices]),
                duration_days=random.randint(1, 5),
                total_hours=random.randint(4, 20)
            )
            for j in range(random.randint(5, 10)):
                 Lesson.objects.create(
                    workshop=workshop, title=f'Session {j+1}: {fake.sentence(nb_words=5)}', order=j,
                    content_type=random.choice(workshop_content_types),
                    content_data={'details': fake.text()}
                )

        # -- 3. Create Learning Paths --
        self.stdout.write('🛤️ Creating learning paths...')
        learning_paths = []
        for i in range(10):
            path = LearningPath.objects.create(
                title=f'Professional Diploma in {random.choice(course_categories)}',
                description=fake.paragraph(nb_sentences=4),
                supervisor=random.choice(supervisors)
            )
            path_courses = random.sample(courses, k=random.randint(3, 7))
            for order, course in enumerate(path_courses):
                LearningPathCourse.objects.create(learning_path=path, course=course, order=order)
            learning_paths.append(path)

        # -- 4. Create B2B Contracts --
        self.stdout.write('💼 Creating B2B contracts...')
        student_pool = list(students)
        for client in b2b_clients:
            num_students_in_contract = random.randint(20, 50)
            if len(student_pool) < num_students_in_contract:
                break # Stop if we run out of students
            contract_students = random.sample(student_pool, k=num_students_in_contract)
            student_pool = [s for s in student_pool if s not in contract_students] # Remove assigned students

            contract = Contract.objects.create(
                title=f'Training Contract for {client.full_name}', client=client,
                start_date=timezone.now() - timedelta(days=random.randint(30, 180)),
                end_date=timezone.now() + timedelta(days=365)
            )
            contract.enrolled_students.set(contract_students)
            contract.learning_paths.add(random.choice(learning_paths))

        # -- 5. Create Enrollments and Simulate Progress --
        self.stdout.write('📈 Creating enrollments and simulating progress...')
        for student in tqdm(random.sample(students, k=400), 'Enrolling students'):
            course_to_enroll = random.choice(courses)
            enrollment, created = Enrollment.objects.get_or_create(student=student, course=course_to_enroll)

            if created:
                lessons_in_course = list(course_to_enroll.lessons.all())
                if lessons_in_course:
                    completed_count = int(len(lessons_in_course) * random.uniform(0.1, 0.99))
                    lessons_to_complete = random.sample(lessons_in_course, k=completed_count)

                    for lesson in lessons_to_complete:
                        LessonProgress.objects.create(
                            enrollment=enrollment, 
                            lesson=lesson,
                            status=LessonProgress.ProgressStatus.COMPLETED,
                            attendance_date=timezone.now() - timedelta(days=random.randint(1, 30))
                        )

                    calculate_progress(enrollment.id)

        self.stdout.write(self.style.SUCCESS('✅ Database seeding complete! The system is ready for testing.'))