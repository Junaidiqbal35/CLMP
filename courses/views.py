from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView
from django.views.generic.base import TemplateResponseMixin, View
from django.apps import apps
from .forms import ModuleFormSet, CourseEnrollForm, CommentForm
from .models import Course, Content, Module, Category, Comment
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, \
    DeleteView, FormView


class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request, category=None):
        categories = Category.objects.annotate(
            total_courses=Count('courses'))
        courses = Course.objects.annotate(
            total_modules=Count('modules'))
        if category:
            category = get_object_or_404(Category, slug=category)
            courses = courses.filter(category=category)
        try:
            if request.user.is_teacher:
                return redirect('manage_course_list')
        except Exception:
            pass
        return self.render_to_response({'categories': categories,
                                        'category': category,
                                        'courses': courses})


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['enroll_form'] = CourseEnrollForm(
            initial={'course': self.object})
        try:
            if Course.objects.filter(students__in=[self.request.user], slug=self.object.slug).exists():
                context['is_enrolled'] = True
        except Exception:
            pass
        return context


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
    fields = ['category', 'title', 'slug', 'overview', 'subscription_package']


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'


class ModuleDetailView(DetailView):
    context_object_name = 'module'
    model = Module
    template_name = 'courses/module/module_detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #
    #     context['comment_form'] = CommentForm()
    #
    #     return context


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


class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__owner=request.user)
        return self.render_to_response({'module': module})


class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(Content,
                                    id=id,
                                    module__course__owner=request.user)
        module = content.module
        content.delete()
        return redirect('module_content_list', module.id)


class ContentUpload(TemplateResponseMixin, View):
    module = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(Content, exclude=['owner', 'module',
                                                   'order',
                                                   'created',
                                                   'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, content_id=None):
        self.module = get_object_or_404(Module,
                                        id=module_id,
                                        course__owner=request.user)

        if content_id:
            self.obj = get_object_or_404(Content,
                                         module=self.module,
                                         id=content_id,
                                         owner=request.user)
            print(self.obj)
        return super().dispatch(request, module_id, content_id)

    def get(self, request, module_id, id=None):
        form = self.get_form(Content, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'object': self.obj})

    def post(self, request, module_id, id=None):
        print(self.obj)
        form = self.get_form(Content,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            print(self.obj)
            obj.module = self.module
            obj.owner = request.user
            obj.save()
            # if not id:
            #     # new content
            #     Content.objects.create(module=self.module,
            #                            item=obj)
            return redirect('module_content_list', self.module.id)
        return self.render_to_response({'form': form,
                                        'object': self.obj})


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form)

    def get_success_url(self):
        return reverse_lazy('student_course_detail',
                            args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get course object
        course = self.get_object()
        if 'module_id' in self.kwargs:
            # get current module
            context['module'] = course.modules.get(
                id=self.kwargs['module_id'])
        else:
            # get first module
            context['module'] = course.modules.all()
        return context

#
# def comment_view(request, content_id):
#     course_video = get_object_or_404(Content, id=content_id)
#     if request.method == 'POST':
#         comment_form = CommentForm(request.POST or None)
#         if comment_form.is_valid():
#             content = request.POST.get('body')
#             comment = Comment.objects.create(course_video=course_video, commenter=request.user, body=content)
#             comment.save()
#             return redirect('index')
#         else:
#             cf = CommentForm()
#
#         context = {
#             'comment_form': cf,
#         }
#         return render(request, 'socio / post_detail.html', context)
