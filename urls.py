"""
URL configuration for test_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from core.views import register_page,login_page,student_page,teacher_page,create_test,add_questions,view_questions,delete_tests,view_questions_2,student_answers_view,student_result_view,enter_test_code,logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_page, name='login_page'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_page, name='register_page'),
    path('student/', student_page, name='student_page'),
    path('teacher/', teacher_page, name='teacher_page'),
    path('create_test/', create_test, name='create_test'),
    path('add-questions/<int:test_id>/',add_questions, name='add_questions'),
    path('view_questions/<int:test_id>/', view_questions, name='view_questions'),
    path('delete_test/<int:test_id>/', delete_tests, name='delete_test'),
    path('view_questions_2/<int:test_id>/', view_questions_2, name='view_questions(2)'),
    path('student-answers/', student_answers_view, name='student_answers'),
    path('student_result/<int:test_id>/<int:score>/<int:total>/', student_result_view, name='student_result'),
    path('enter-code/<int:test_id>/', enter_test_code, name='enter_test_code'),
    path('accounts/', include('allauth.urls')),
    


   
   

]
