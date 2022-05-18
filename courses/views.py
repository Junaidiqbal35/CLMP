from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import modelform_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateResponseMixin, View

from .forms import ModuleFormSet, CourseForm
from .models import Course, Content, Module
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, \
    DeleteView


class CourseView(LoginRequiredMixin, ListView):
    paginate_by = 20
    template_name = "index.html"
    queryset = Course.objects.all()
    context_object_name = 'course'
    model = Course


class OwnerMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course
    fields = ['category', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'
    model = Course

    # def get_formset(self, data=None):
    #     return ModuleFormSet(data=data)
    #
    # def get(self, request, *args, **kwargs):
    #     formset = self.get_formset()
    #     form = CourseForm()
    #     return self.render_to_response({'form': form,
    #                                     'formset': formset})
    #
    # def post(self, request, *args, **kwargs):
    #     formset = self.get_formset(data=request.POST)
    #     form = CourseForm(request.POST)
    #
    #     if formset.is_valid() and form.is_valid():
    #         course = form.save(commit=False)
    #         course.save()
    #         formset.save(course=course)
    #         return redirect('manage_course_list')
    #     else:
    #         print(formset.errors)
    #         print(form.errors)
    #         return self.render_to_response({'form': form,
    #                                         'formset': formset})


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'


class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course,
                             data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course,
                                        id=pk,
                                        owner=request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course,
                                        'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course': self.course,
                                        'formset': formset})


# class CourseModuleCreateView(CreateView):
#     model = Course
#     form_class = ModuleFormSet
#     template_name = 'form.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(CourseModuleCreateView, self).get_context_data(**kwargs)
#         context['formset'] = ModuleFormSet()
#         # context['day_form'] = DayForm()
#         return context
#
#     def post(self, request, *args, **kwargs):
#         formset = self.form_class(request.POST)
#         if formset.is_valid():
#             return self.form_valid(formset)
#
#     def form_valid(self, formset):
#         instances = formset.save(commit=False)
#         for instance in instances:
#             # instance.day = day
#             instance.save()
#         return HttpResponseRedirect('/dashboard/')


class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = Content
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['owner',
                                                 'order',
                                                 'created',
                                                 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, id=None):
        self.module = get_object_or_404(Module,
                                        id=module_id,
                                        course__owner=request.user)

        if id:
            self.obj = get_object_or_404(
                                         id=id,
                                         owner=request.user)
        return super().dispatch(request, module_id, id)
