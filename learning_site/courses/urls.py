from django.contrib import admin
from django.urls import path, include, re_path

from . import views


app_name = 'courses'


urlpatterns = [
    path('', views.course_list, name="course_list"),
    path('<int:pk>/', views.course_detail, name="course_detail"),
    path('<int:course_pk>/t<int:pk>/', views.text_detail, name="text_detail"),
    path('<int:course_pk>/q<int:pk>/', views.quiz_detail, name="quiz_detail"),
    path('<int:course_pk>/edit_quiz/<int:pk>/', views.quiz_edit, name="quiz_edit"),
    path('<int:quiz_pk>/edit_question/<int:pk>/', views.question_edit, name="question_edit"),
    path('<int:course_pk>/create_quiz/', views.quiz_create, name="quiz_create"),
    path('<int:question_pk>/create_answer/', views.answer_create,  name="create_answer"),
    path('by/<teacher>', views.courses_by_teacher, name="by_teacher"),
    path('search/', views.search, name="search"),
    re_path(r'(?P<quiz_pk>\d+)/create_question/(?P<question_type>mc|tf)/$', views.create_question, name='create_question'),
]


