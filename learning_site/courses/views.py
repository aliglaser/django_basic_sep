from itertools import chain

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Sum

from . import forms
from . import models

# Create your views here.
def course_list(request):
	courses = models.Course.objects.filter(
		published=True
	).annotate(
		total_steps=Count('text', distinct=True)+Count('quiz', distinct=True)
	)
	email = 'questions@learning_site.com'
	return render(request, 'courses/course_list.html', {'courses':courses, 'email':email})


def course_detail(request, pk):
	try:
		course = models.Course.objects.prefetch_related(
			'quiz_set', 'text_set'
		).get(pk=pk, published=True)
	except models.Course.DoesNotExist:
		raise Http404
	else:	
		steps = sorted(chain(course.text_set.all(), course.quiz_set.all()), key=lambda step: step.order)
	return render(request, 'courses/course_detail.html', {'course':course, 'steps':steps})	


def text_detail(request, course_pk, pk):
	step = get_object_or_404(models.Text, course_id=course_pk, pk=pk, course__published=True)	
	return render(request, 'courses/text_detail.html', {'step':step})



def quiz_detail(request, course_pk, pk):
	step = get_object_or_404(models.Quiz, course_id=course_pk, pk=pk, course__published=True)	
	return render(request, 'courses/quiz_detail.html', {'step':step})


@login_required
def quiz_create(request, course_pk):
	course = get_object_or_404(models.Course, pk=course_pk, published=True)
	form = forms.QuizForm()

	if request.method=='POST':
		form = forms.QuizForm(request.POST)
		if form.is_valid():
			quiz = form.save(commit=False)
			quiz.course = course
			quiz.save()
			messages.add_message(request, messages.SUCCESS, "Quiz added!")
			return HttpResponseRedirect(quiz.get_absolute_url())
	return render(request, 'courses/quiz_form.html', {'form':form, 'course':course})		



@login_required
def quiz_edit(request, course_pk, pk):
	quiz = get_object_or_404(models.Quiz, course_id=course_pk, pk=pk, course__published=True)
	form = forms.QuizForm(instance=quiz)

	if request.method == 'POST':
		form = forms.QuizForm(instance=quiz, data=request.POST)
		if form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, "Quiz edited!")
			return HttpResponseRedirect(quiz.get_absolute_url())
	return render(request, 'courses/quiz_form.html', {'form':form, 'course':quiz.course})		


@login_required
def create_question(request, quiz_pk, question_type):
	quiz = get_object_or_404(models.Quiz, pk=quiz_pk, course__published=True)
	if question_type == 'tf':
		form_class = forms.TrueFalseQuestionForm
	else:
		form_class = forms.MultipleChoiceQuestionForm

	form = form_class()
	answer_forms = forms.AnswerInlineFormSet(
		request.POST,
		queryset=models.Answer.objects.none()
	)

	if request.method == "POST":
		form = form_class(request.POST)
		answer_forms = forms.AnswerInlineFormSet(
		request.POST,
		queryset=models.Answer.objects.none()
	)
		if form.is_valid() and answer_forms.is_valid():
			question=form.save(commit=False)	
			question.quiz = quiz
			question.save()
			answers = forms.answer_forms.save(commit=False)
			for answer in answers:
				answer.question = question
				answer.save()
			messages.add_message(request, messages.SUCCESS, "Question Created!")
			return HttpResponseRedirect(quiz.get_absolute_url())
	return render(request, 'courses/question_form.html', {'form':form, 'quiz':quiz, 'formset':answer_forms})	



@login_required
def question_edit(request, quiz_pk, pk):
	question = get_object_or_404(models.Question, quiz_id=quiz_pk, pk=pk)
	if hasattr(question, 'truefalsequestion'):
		form_class = forms.TrueFalseQuestionForm
	else:
		form_class = forms.MultipleChoiceQuestionForm
	form = form_class(instance = question)
	answer_forms = forms.AnswerInlineFormSet(queryset=form.instance.answer_set.all())

	if request.method == 'POST':
		form = form_class(instance = question, data = request.POST)
		answer_forms = forms.AnswerInlineFormSet(request.POST, queryset=form.instance.answer_set.all())
		if form.is_valid() and answer_forms.is_valid():
			form.save()
			answers = answer_forms.save(commit=False)
			for answer in answers:
				answer.question = question
				answer.save()
			messages.add_message(request, messages.SUCCESS, 'Successfully added!!!!')
			return HttpResponseRedirect(question.quiz.get_absolute_url())
	return render(request, 'courses/question_form.html', {'form':form, 'quiz':question.quiz, 'formset':answer_forms})		

@login_required
def answer_create(request, question_pk):
	question = get_object_or_404(models.Question, pk=question_pk)
	formset = forms.AnswerFormSet(queryset=question.answer_set.all())

	if request.method == 'POST':
		formset = forms.AnswerForm(request.POST, queryset=question.answer_set.all())
		if formset.is_valid():
			answers = formset.save(commit=False)
			for answer in answers:
				answer.question = question
				answer.save()
			messages.add_message(request, messages.SUCCESS, 'Answers added')
			return HttpResponseRedirect(question.get_absolute_url())
	return render(request, 'courses/answer_form.html', {'formset':formset, 'question':question})		



def courses_by_teacher(request, teacher):
	courses = models.Course.objects.filter(teacher__username=teacher, published=True)
	return render(request, 'courses/course_list.html', {'courses':courses})


def search(request):
	term = request.GET.get('q')
	courses = models.Course.objects.filter(published=True).filter(Q(title__icontains=term)|Q(description__icontains=term))
	return render(request, 'courses/course_list.html', {'courses':courses})


