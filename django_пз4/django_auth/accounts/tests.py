from django.contrib.auth.models import User
from django.test import TestCase


class ProfileAccessTests(TestCase):
    def setUp(self):
        User.objects.create_user(username="student1", password="Kuznetsova2026!")

    def test_profile_redirects_anonymous_user(self):
        response = self.client.get("/profile/")
        self.assertRedirects(response, "/accounts/login/?next=/profile/")

    def test_login_page_opens(self):
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)

    def test_profile_after_login(self):
        self.client.login(username="student1", password="Kuznetsova2026!")
        response = self.client.get("/profile/")
        self.assertContains(response, "student1")

    def test_logout_redirects_to_login(self):
        self.client.login(username="student1", password="Kuznetsova2026!")
        response = self.client.post("/accounts/logout/")
        self.assertRedirects(response, "/accounts/login/")


class CourseOrmTests(TestCase):
    def setUp(self):
        from .models import Course, Department, StudentProfile
        self.user = User.objects.create_user(username="student2", password="Kuznetsova2026!")
        self.dep = Department.objects.create(name="Информационные технологии")
        self.course = Course.objects.create(title="Базы данных", department=self.dep)
        self.profile = StudentProfile.objects.create(user=self.user, department=self.dep)
        self.profile.courses.add(self.course)

    def test_related_objects(self):
        self.assertIn(self.course, self.dep.courses.all())
        self.assertEqual(self.user.student_profile, self.profile)
        self.assertIn(self.profile, self.course.students.all())

    def test_course_list_requires_login(self):
        response = self.client.get("/courses/")
        self.assertRedirects(response, "/accounts/login/?next=/courses/")

    def test_course_list_shows_courses(self):
        self.client.login(username="student2", password="Kuznetsova2026!")
        response = self.client.get("/courses/")
        self.assertContains(response, "Базы данных")
        self.assertContains(response, "Информационные технологии")
