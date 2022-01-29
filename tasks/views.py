from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.forms import ModelForm, ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from tasks.models import Task


# * Traditional Login Page: Form consists of `username` and `password` to authenticate into the `task_manager`
class UserLoginView(LoginView):
    template_name = "user/login.html"


# * Traditional Signup Page: Form consists of `username`, `password` and `confirm password` to create a new user in the `task_manager`
class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "user/signup.html"
    success_url = "/user/login"


# * Learning Cookies: Simple view counter tied with each session
def session_storage_view(request):
    total_views = request.session.get("total_views", 0)
    request.session["total_views"] = total_views + 1
    return HttpResponse(f"Total views is {total_views} and user is {request.user}")


# * Authorisation (Combined Mixin): To allow access only to users who are 'logged in' and allow them only to view their respective 'tasks'
class AuthorisedTaskManager(LoginRequiredMixin):
    def get_queryset(self):
        return Task.objects.filter(deleted=False, user=self.request.user)


# * Task Create Form: Customizing contents of `ModelForm`
class TaskCreateForm(ModelForm):

    # ? clean_<attribute>: access to cleaning that <attribute>
    # * Cleaning Title Attribute: Access contents of Form from `cleaned_data` dictionary
    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) < 5:
            raise ValidationError("Data too small")
        return title

    # ? Meta data for `TaskCreateForm` provided inside
    class Meta:
        model = Task
        fields = ["title", "description", "completed", "priority"]


# * Create Task Page: Form consisting of `Task` attributes to create a new record in the database
class GenericTaskCreateView(CreateView):
    form_class = TaskCreateForm
    template_name = "task/create.html"
    success_url = "/tasks"

    # ? Overriding
    # * Associate `User` with `Task`: After storing contents of `form`, before `success_url`
    def form_valid(self, form):
        """If the form is valid, save the associated model."""

        conflict = form.cleaned_data["priority"]
        task = Task.objects.filter(deleted=False, priority=conflict)
        print("Before Loop:", task)
        while task.exists():
            conflict += 1
            task = Task.objects.filter(deleted=False, priority=conflict)
            print("Conflict:", conflict)
            print("Task:", task)
        print(form.cleaned_data["priority"], conflict)

        for i in range(conflict, form.cleaned_data["priority"], -1):
            task = Task.objects.filter(deleted=False, priority=i - 1)
            print(task)
            task.update(priority=i)

        # * Save newly created object
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


# * List Pending Tasks Page: `ListView` of all pending `Task` records available in the database
class GenericPendingTaskView(LoginRequiredMixin, ListView):
    queryset = Task.objects.filter(completed=False, deleted=False).order_by("-priority")
    template_name = "task/tasks.html"
    context_object_name = "tasks"
    # * Pagination Feature using `paginator`
    paginate_by = 5

    # * Search Feature: Find pending `Task` with matching case-insensitive `title` attribute
    # def get_queryset(self):
    #     search_term = self.request.GET.get("search")
    #     tasks = Task.objects.filter(
    #         completed=False, deleted=False, user=self.request.user
    #     )
    #     if search_term:
    #         tasks = tasks.filter(title__icontains=search_term)
    #     return tasks.order_by("-priority")


# * Update Task Page: Form consisting of `Task` attributes with their pre-existing data
class GenericTaskUpdateView(AuthorisedTaskManager, UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "task/update.html"
    success_url = "/all-tasks"


# * Delete Task Page: Form consists of `confirm`ation button with POST to be a safe-method as soft-deletion of `Task` causes side-effect
class GenericTaskDeleteView(AuthorisedTaskManager, DeleteView):
    model = Task
    template_name = "task/delete.html"
    success_url = "/all-tasks"


# * Detail Task Page: Details of specific `Task` model with context-variable as `object`
class GenericTaskDetailView(AuthorisedTaskManager, DetailView):
    model = Task
    template_name = "task/detail.html"


# class TaskView(View):
#     def get(self, request):
#         search_term = request.GET.get("search")
#         tasks = Task.objects.filter(completed=False).filter(deleted=False)
#         if search_term:
#             tasks = tasks.filter(title__icontains=search_term)
#         return render(request, "tasks.html", {"tasks": tasks})

#     def post(self, request):
#         pass


# class CreateTaskView(View):
#     def get(self, request):
#         return render(request, "task_create.html")

#     def post(self, request):
#         task_value = request.POST.get("task")
#         task_obj = Task(title=task_value)
#         task_obj.save()
#         return HttpResponseRedirect("/tasks")


# def tasks_view(request):
#     search_term = request.GET.get("search")
#     tasks = Task.objects.filter(completed=False).filter(deleted=False)
#     if search_term:
#         tasks = tasks.filter(title__icontains=search_term)
#     return render(request, "tasks.html", {"tasks": tasks})


# def add_task_view(request):
#     task_value = request.GET.get("task")
#     task_obj = Task(title=task_value)
#     task_obj.save()
#     return HttpResponseRedirect("/tasks")


# def delete_task_view(request, index):
#     # Task.object.filter(id=index).delete()

#     # Soft Deletion
#     Task.objects.filter(id=index).update(deleted=True)
#     return HttpResponseRedirect("/tasks")

# * List All Tasks Page: `ListView` of all `Task` records available in the database
class GenericAllTaskView(LoginRequiredMixin, ListView):
    queryset = Task.objects.filter(deleted=False).order_by("-priority")
    template_name = "task/all.html"
    context_object_name = "tasks"
    # * Pagination Feature using `paginator`
    paginate_by = 5


# * List Completed Tasks Page: `ListView` of all completed `Task` records available in the database
class GenericCompletedTaskView(LoginRequiredMixin, ListView):
    queryset = Task.objects.filter(completed=True, deleted=False).order_by("-priority")
    template_name = "task/completed.html"
    context_object_name = "tasks"
    # * Pagination Feature using `paginator`
    paginate_by = 5


# def complete_task_view(request, index):
#     Task.objects.filter(id=index).update(completed=True)
#     return HttpResponseRedirect("/tasks")


# def completed_tasks_view(request):
#     completed_tasks = Task.objects.filter(completed=True, deleted=False)
#     return render(request, "task/completed.html", {"tasks": completed_tasks})


# def all_tasks_view(request):
#     tasks = Task.objects.filter(completed=False, deleted=False)
#     completed_tasks = Task.objects.filter(completed=True, deleted=False)
#     return render(
#         request, "task/all.html", {"tasks": tasks, "completed_tasks": completed_tasks}
#     )
