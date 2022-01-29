"""task_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.contrib.auth.views import LogoutView
from django.urls import path
from tasks.views import (
    # CreateTaskView,
    GenericTaskCreateView,
    GenericTaskDeleteView,
    GenericTaskDetailView,
    GenericTaskUpdateView,
    GenericPendingTaskView,
    GenericAllTaskView,
    GenericCompletedTaskView,
    UserCreateView,
    UserLoginView,
    UserLogoutView,
    # add_task_view,
    # all_tasks_view,
    # complete_task_view,
    # completed_tasks_view,
    # delete_task_view,
    session_storage_view,
    # tasks_view,
)

# ! Chrome: Inserts trailing slash before requesting the Django Server

urlpatterns = [
    # ! Admin
    path("admin/", admin.site.urls),
    # ! Task
    path("tasks/", GenericPendingTaskView.as_view()),
    path("create-task/", GenericTaskCreateView.as_view()),
    path("update-task/<pk>/", GenericTaskUpdateView.as_view()),
    path("detail-task/<pk>/", GenericTaskDetailView.as_view()),
    path("delete-task/<pk>/", GenericTaskDeleteView.as_view()),
    # TODO: Complete route "complete-task/<pk>": To mark as completed
    # path("complete_task/<int:index>/", complete_task_view),
    # ! User
    path("user/signup/", UserCreateView.as_view()),
    path("user/login/", UserLoginView.as_view()),
    path("user/logout/", LogoutView.as_view()),
    # ! Additional
    path("completed-tasks/", GenericCompletedTaskView.as_view()),
    # path("add-task", add_task_view),
    path("all-tasks/", GenericAllTaskView.as_view()),
    path("sessiontest/", session_storage_view),
]
