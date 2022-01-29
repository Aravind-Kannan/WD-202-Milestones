from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from tasks.views import (
    GenericAllTaskView,
    GenericCompletedTaskView,
    GenericPendingTaskView,
    GenericTaskCreateView,
    GenericTaskDeleteView,
    GenericTaskDetailView,
    GenericTaskUpdateView,
    UserCreateView,
    UserLoginView,
    session_storage_view,
)

# ! Chrome: Inserts trailing slash before requesting the Django Server

urlpatterns = [
    # ! Admin
    path("admin/", admin.site.urls),
    # ! Task
    ## ! Landing
    path("all-tasks/", GenericAllTaskView.as_view()),
    path("tasks/", GenericPendingTaskView.as_view()),
    path("completed-tasks/", GenericCompletedTaskView.as_view()),
    ## ! CRUD with Task Model
    path("create-task/", GenericTaskCreateView.as_view()),
    path("update-task/<pk>/", GenericTaskUpdateView.as_view()),
    path("detail-task/<pk>/", GenericTaskDetailView.as_view()),
    path("delete-task/<pk>/", GenericTaskDeleteView.as_view()),
    # ! User
    path("user/signup/", UserCreateView.as_view()),
    path("user/login/", UserLoginView.as_view()),
    path("user/logout/", LogoutView.as_view()),
    # ! Additional
    path("sessiontest/", session_storage_view),
]
