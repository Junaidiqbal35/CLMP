from allauth.account.views import SignupView
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import DetailView

from accounts.forms import CreateUserForm, StudentForm, TeacherForm
from accounts.models import User


class StudentAddView(SignupView):
    """
    Creates new employee
    """
    template_name = 'students/registration.html'
    form_class = CreateUserForm
    work_form_class = StudentForm

    def get(self, request, *args, **kwargs):
        # Use RequestContext instead of render_to_response from 3.0
        return render(request, self.template_name, {'form': self.form_class, 'work_form': self.work_form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        work_form = self.work_form_class(request.POST)
        print(form.errors)
        if form.is_valid() and work_form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_student = True
            user.save()

            # user = U.objects.get(email=user.email)
            student = work_form.save(commit=False)
            student.user = user
            student.save()
            # complete_signup(request, user, app_settings.EMAIL_VERIFICATION, "/")

            return redirect('courses')
        return render(request, self.template_name, {'form': form, 'work_form': work_form})


class TeacherAddView(SignupView):
    template_name = 'teacher/registration.html'
    form_class = CreateUserForm
    work_form_class = TeacherForm

    def get(self, request, *args, **kwargs):
        # Use RequestContext instead of render_to_response from 3.0
        return render(request, self.template_name, {'form': self.form_class, 'work_form': self.work_form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        work_form = self.work_form_class(request.POST)
        if form.is_valid() and work_form.is_valid():
            user = form.save(commit=False)
            print(form.cleaned_data['password'])
            user.set_password(form.cleaned_data['password'])

            user.is_teacher = True
            group = Group.objects.get(name='teacher')
            user.groups.add(group)
            user.save()

            # user = CustomUser.objects.get(email=user.email)
            teacher = work_form.save(commit=False)
            teacher.user = user
            # complete_signup(request, user, app_settings.EMAIL_VERIFICATION, "/")

            teacher.save()


            return redirect('courses')
        return render(request, self.template_name, {'form': form, 'work_form': work_form})


class Profile(DetailView):
    template_name = "account/../templates/base_student_dashboard.html"
    queryset = User.objects.all()
    context_object_name = 'user'

    def get_object(self):
        return self.request.user
