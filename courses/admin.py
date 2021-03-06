from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Course, Module, Content, Comment, CourseProgress


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created']
    list_filter = ['created', 'category']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]


admin.site.register(Content)
admin.site.register(Comment)
admin.site.register(Module)
admin.site.register(CourseProgress)

