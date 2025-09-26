# apps/core/management/commands/seed_data.py

import random
import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from faker import Faker
from tqdm import tqdm

from apps.users.models import CustomUser
from apps.learning.models import Course, Lesson, LearningPath, LearningPathCourse
from apps.enrollment.models import Enrollment, CompletedLesson
from apps.contracts.models import Contract
from apps.enrollment.services import calculate_progress

class Command(BaseCommand):
    help = 'Seeds the database with a smaller, more focused and logical set of test data.'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        if CustomUser.objects.count() > 1:
            self.stdout.write(self.style.WARNING('Database already contains data. Seeding skipped.'))
            return

        self.stdout.write(self.style.SUCCESS('🚀 Starting focused database seeding...'))
        fake = Faker()
        password = make_password('password')

        # -- 1. Create Focused Users --
        self.stdout.write('👤 Creating a focused set of users...')
        supervisors = CustomUser.objects.bulk_create([
            CustomUser(username='supervisor.one', email='supervisor.one@example.com', password=password, role=CustomUser.Roles.SUPERVISOR, full_name='Sarah Supervisor'),
            CustomUser(username='supervisor.two', email='supervisor.two@example.com', password=password, role=CustomUser.Roles.SUPERVISOR, full_name='Sam Supervisor'),
        ])
        instructors = CustomUser.objects.bulk_create([
            CustomUser(username='instructor.python', email='instructor.python@example.com', password=password, role=CustomUser.Roles.INSTRUCTOR, full_name='Dr. Python Coder'),
            CustomUser(username='instructor.marketing', email='instructor.marketing@example.com', password=password, role=CustomUser.Roles.INSTRUCTOR, full_name='Marketa Digital'),
            CustomUser(username='instructor.design', email='instructor.design@example.com', password=password, role=CustomUser.Roles.INSTRUCTOR, full_name='Desiree Signer'),
            CustomUser(username='instructor.business', email='instructor.business@example.com', password=password, role=CustomUser.Roles.INSTRUCTOR, full_name='Adam Capital'),
            CustomUser(username='instructor.datasci', email='instructor.datasci@example.com', password=password, role=CustomUser.Roles.INSTRUCTOR, full_name='Data Dan'),
        ])
        students = CustomUser.objects.bulk_create([CustomUser(username=f'student.{i}', email=f'student.{i}@example.com', password=password, role=CustomUser.Roles.STUDENT, full_name=fake.name()) for i in range(30)])
        b2b_clients = CustomUser.objects.bulk_create([
            CustomUser(username='client.techcorp', email='contact@techcorp.com', password=password, role=CustomUser.Roles.THIRD_PARTY, full_name='TechCorp Inc.'),
            CustomUser(username='client.bizsolutions', email='contact@bizsolutions.com', password=password, role=CustomUser.Roles.THIRD_PARTY, full_name='Biz Solutions Ltd.'),
        ])

        # -- 2. Create Logical Courses --
        self.stdout.write('📚 Creating logical courses and lessons...')
        # (This section remains unchanged)
        courses = []
        course_defs = [
            {'title': 'Python for Beginners', 'instructor': instructors[0], 'category': 'Programming'},
            {'title': 'Advanced Django', 'instructor': instructors[0], 'category': 'Programming'},
            {'title': 'SEO Masterclass', 'instructor': instructors[1], 'category': 'Marketing'},
            {'title': 'Social Media Strategy', 'instructor': instructors[1], 'category': 'Marketing'},
            {'title': 'UI/UX Design Fundamentals', 'instructor': instructors[2], 'category': 'Design'},
            {'title': 'Introduction to Financial Modeling', 'instructor': instructors[3], 'category': 'Business'},
            {'title': 'Machine Learning with Python', 'instructor': instructors[4], 'category': 'Data Science'},
        ]
        for i in range(13):
            instr = random.choice(instructors)
            course_defs.append({'title': f'{instr.full_name.split()[1]}\'s Guide to {fake.job()}', 'instructor': instr, 'category': random.choice(['Programming', 'Business'])})
        for i, c_def in enumerate(tqdm(course_defs, 'Creating Courses')):
            course = Course.objects.create(
                title=c_def['title'], slug=f'course-{fake.slug()}-{i}', description=fake.paragraph(nb_sentences=5),
                instructor=c_def['instructor'], category=c_def['category'], status=Course.CourseStatus.PUBLISHED
            )
            courses.append(course)
            for j in range(random.randint(8, 15)):
                Lesson.objects.create(course=course, title=f'Module {j+1}: {fake.sentence(nb_words=4)}', order=j, content_type=random.choice([Lesson.ContentType.VIDEO, Lesson.ContentType.TEXT]), content_data={'url': fake.url()})

        # -- 3. Create Logical Learning Paths --
        self.stdout.write('🛤️ Creating logical learning paths...')
        # === THE FIX IS HERE ===
        path_course_relations = []
        
        web_dev_path = LearningPath.objects.create(title='Web Development Track', description='Become a full-stack web developer.', supervisor=supervisors[0])
        web_dev_courses = [courses[0], courses[1], courses[6]] # Python, Django, Machine Learning
        for order, course in enumerate(web_dev_courses):
            path_course_relations.append(LearningPathCourse(learning_path=web_dev_path, course=course, order=order))

        marketing_path = LearningPath.objects.create(title='Digital Marketing Certificate', description='Master the art of digital marketing.', supervisor=supervisors[1])
        marketing_courses = [courses[2], courses[3]] # SEO, Social Media
        for order, course in enumerate(marketing_courses):
            path_course_relations.append(LearningPathCourse(learning_path=marketing_path, course=course, order=order))
            
        LearningPathCourse.objects.bulk_create(path_course_relations)
        
        # -- 4. Create Contracts and Link Employees --
        self.stdout.write('💼 Creating B2B contracts and linking employees...')
        # (This section remains unchanged, but we'll re-run it for a clean state)
        tech_corp_contract = Contract.objects.create(title='TechCorp Employee Training 2025', client=b2b_clients[0], start_date=timezone.now(), end_date=timezone.now() + datetime.timedelta(days=365))
        tech_corp_contract.enrolled_students.set(students[0:10])
        tech_corp_contract.learning_paths.add(web_dev_path)

        biz_solutions_contract = Contract.objects.create(title='Biz Solutions Marketing Upskill', client=b2b_clients[1], start_date=timezone.now(), end_date=timezone.now() + datetime.timedelta(days=365))
        biz_solutions_contract.enrolled_students.set(students[10:20])
        biz_solutions_contract.learning_paths.add(marketing_path)

        # -- 5. Enroll students and simulate progress --
        self.stdout.write('📈 Enrolling students and simulating progress...')
        # (This section remains unchanged)
        for student in tqdm(students, 'Enrolling students'):
            course_to_enroll = random.choice(courses)
            enrollment, created = Enrollment.objects.get_or_create(student=student, course=course_to_enroll)
            if created and random.random() > 0.5:
                lessons_in_course = list(course_to_enroll.lessons.all())
                if lessons_in_course:
                    completed_count = int(len(lessons_in_course) * random.uniform(0.2, 1.0))
                    for lesson in random.sample(lessons_in_course, k=completed_count):
                        CompletedLesson.objects.create(enrollment=enrollment, lesson=lesson)
                    calculate_progress(enrollment.id)
        
        self.stdout.write(self.style.SUCCESS('✅ Focused database seeding complete!'))