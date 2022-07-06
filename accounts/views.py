from allauth.account.views import SignupView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import DetailView, UpdateView

from accounts.forms import CreateUserForm, StudentForm, TeacherForm, UpdateTeacherForm, UpdateUserForm
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

            return redirect('account_login')
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
        work_form = self.work_form_class(request.POST, request.FILES)
        if form.is_valid() and work_form.is_valid():
            user = form.save(commit=False)
            print(form.cleaned_data['password'])
            user.set_password(form.cleaned_data['password'])

            user.is_teacher = True

            user.save()
            group = Group.objects.get(name='teacher')
            user.groups.add(group)

            # user = CustomUser.objects.get(email=user.email)
            teacher = work_form.save(commit=False)
            teacher.user = user
            # complete_signup(request, user, app_settings.EMAIL_VERIFICATION, "/")

            teacher.save()

            return redirect('account_login')
        return render(request, self.template_name, {'form': form, 'work_form': work_form})


class UserProfile(LoginRequiredMixin, DetailView):
    template_name = "account/profile.html"
    queryset = User.objects.all()
    context_object_name = 'profile'
    slug_field = 'id'

    model = User


class TeacherProfileUpdateView(UpdateView):
    model = User
    template_name = 'teacher/profile.html'
    form_class = UpdateUserForm
    work_form_class = UpdateTeacherForm

    def get(self, request, *args, **kwargs):
        # Use RequestContext instead of render_to_response from 3.0
        return render(request, self.template_name, {'form': self.form_class(instance=request.user),
                                                    'work_form': self.work_form_class(instance=request.user.teacher_user)})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user)
        work_form = self.work_form_class(request.POST, request.FILES, instance=request.user.teacher_user)
        if form.is_valid() and work_form.is_valid():
            form.save()
            work_form.save()
            messages.success(request, 'Your profile is updated successfully')

            return redirect('profile', request.user.id)

        return render(request, self.template_name, {'form': form, 'work_form': work_form})


class StudentProfileUpdateView(UpdateView):
    model = User
    template_name = 'students/student_profile.html'
    form_class = UpdateUserForm
    work_form_class = UpdateTeacherForm

    def get(self, request, *args, **kwargs):
        # Use RequestContext instead of render_to_response from 3.0
        return render(request, self.template_name, {'form': self.form_class(instance=request.user),
                                                    'work_form': self.work_form_class(instance=request.user.student_user)})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user)
        work_form = self.work_form_class(request.POST, request.FILES, instance=request.user.student_user)
        if form.is_valid() and work_form.is_valid():
            form.save()
            work_form.save()
            messages.success(request, 'Your profile is updated successfully')

            return redirect('profile', request.user.id)

        return render(request, self.template_name, {'form': form, 'work_form': work_form})