from multiprocessing.connection import wait
from time import sleep
from django.contrib.auth.models import AnonymousUser
from django.test import LiveServerTestCase, RequestFactory, TestCase
from rest_framework import status
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from tasks.models import Task, User
from tasks.views import (
    GenericAllTaskView,
    GenericCompletedTaskView,
    GenericPendingTaskView,
    TaskCreateForm,
)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestCases(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="bruce_wayne", email="bruce@wayne.org", password="i_am_batman"
        )

    def test_view_user_login(self):
        response = self.client.get("/user/login/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_user_signup(self):
        response = self.client.get("/user/signup/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_pending_tasks_no_access(self):
        request = self.factory.get("/tasks/")
        request.user = AnonymousUser()
        response = GenericPendingTaskView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, "/user/login?next=/tasks/")

    def test_view_pending_tasks(self):
        request = self.factory.get("/tasks/")
        request.user = self.user
        response = GenericPendingTaskView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_all_tasks(self):
        request = self.factory.get("/all-tasks/")
        request.user = self.user
        response = GenericAllTaskView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_completed_tasks(self):
        request = self.factory.get("/completed-tasks/")
        request.user = self.user
        response = GenericCompletedTaskView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_session_storage(self):
        response = self.client.get("/sessiontest/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# Trying Selenium
class HostTestCases(LiveServerTestCase):
    def setUp(self):
        user = User.objects.create(username="bruce_wayne", email="bruce@wayne.org")
        user.password = "i_am_batman"
        user.save()

    def test_userlogin_page(self):
        driver = webdriver.Chrome()

        driver.get("http://127.0.0.1:8000/user/login/")
        username = driver.find_element_by_id("id_username")
        password = driver.find_element_by_id("id_password")
        submit = driver.find_element_by_xpath("/html/body/div/div/form/button")

        username.send_keys("bruce_wayne")
        password.send_keys("i_am_batman")
        submit.send_keys(Keys.RETURN)

        self.assertEqual(Task.objects.filter(user=self.user).count(), 0)
