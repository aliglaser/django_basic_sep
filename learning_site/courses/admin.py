from datetime import date
from django.contrib import admin

# Register your models here.
from . import models


def make_published(modeladmin, request, queryset):
	queryset.update(status='p', published = True)


class YearListFilter(admin.SimpleListFilter):
	title = 'year_created'
	parameter_name = 'year'

	def lookups(self, request, model_admin):
		return (
			('2018', '2018'),
			('2019', '2019'),
		)

	def queryset(self, request, queryset):
		if self.value() == '2018':
			return queryset.filter(created_at__gte=date(2018,1,1), created_at__lte=date(2018,12,31))
		if self.value() == '2019':
			return queryset.filter(created_at__gte=date(2019,1,1), created_at__lte=date(2019,12,31))


class TextInline(admin.StackedInline):
	model = models.Text


class CourseAdmin(admin.ModelAdmin):
	inlines = [TextInline,]

	search_fields = ['title', 'description']

	list_filter = ['created_at', 'published', YearListFilter]

	list_display = ['title', 'created_at', 'published','time_to_complete', 'status']

	list_editable = ['published']

	actions = [make_published]

	class Media:
		js = ('js/vendor/markdown.js', 'js/preview.js')
		css = {
			'all' : ('css/preview.css',), 
		}

class QuizAdmin(admin.ModelAdmin):
	fields = ['course', 'description', 'order', 'total_question']




class AnswerInline(admin.TabularInline):
	model = models.Answer	


class QuestionAdmin(admin.ModelAdmin):
	inlines = [AnswerInline,]

	search_fields = ['prompt']

	list_display = ['prompt', 'quiz', 'order']

	list_editable = ['quiz', 'order']

	radio_fields = {'quiz':admin.HORIZONTAL }


class TextAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {
			'fields' : ('course', 'title', 'order', 'description')
			}),
		('Add content', {
			'fields' : ('content',),
			'classes' : ('collapse',)
			})
	)

admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.Text, TextAdmin)
admin.site.register(models.Quiz, QuizAdmin)
admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Answer)