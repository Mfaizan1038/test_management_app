from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from .models import User,Test,Question,StudentAnswer
from django.contrib.auth.decorators import login_required


def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get("first_Name")
        last_name = request.POST.get("last_Name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")  

        if role not in ['Teacher', 'Student']:
            messages.error(request, "Please select a valid role")
            return redirect('/register/')

        user = User.objects.filter(username=username)
        if user.exists():
            messages.error(request, "Username already taken")
            return redirect('/register/')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            role=role  
        )
        user.set_password(password)
        user.save()
        messages.success(request, "Account created successfully")
        return redirect('/login/')  

    return render(request, 'register.html')


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        selected_role = request.POST.get("role") 

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid username")
            return redirect('/login/')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Invalid password")
            return redirect('/login/')
        else:
           
            if user.role != selected_role:
                messages.error(request, f"Incorrect role selected. You are registered as a {user.role}.")
                return redirect('/login/')

            login(request, user)

            if user.role == 'Teacher':
                return redirect('/teacher/')
            elif user.role == 'Student':
                return redirect('/student/')
            else:
                return redirect('/home/')

    return render(request, 'login.html')

@login_required
def student_page(request):
    tests = Test.objects.all()  
    if request.user.role != 'Student':
        return redirect('/error/')
    return render(request, 'student.html', {'tests': tests})

@login_required
def teacher_page(request):
    tests = Test.objects.filter(created_by=request.user)
    if request.user.role != 'Teacher':
        return redirect('/error/')
    return render(request, 'teacher.html', {'tests': tests})


def create_test(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        is_public = request.POST.get('is_public') == 'on'
        code = request.POST.get('code', '')
        already_exist=Test.objects.filter(code=code).exists()
        if already_exist:
            messages.error(request, " this code has been taken")
            return render(request, 'create_test.html')
            
        if not is_public and not code:
            messages.error(request, " code is required for private tests.")
            return render(request, 'create_test.html')
        if is_public:
            code =''

        new_test = Test.objects.create(
            title=title,
            description=description,
            is_public=is_public,
            code=code,
            created_by=request.user
        )
        return redirect(f'/add-questions/{new_test.id}/')
    
    return render(request, 'create_test.html')

@login_required
def add_questions(request, test_id):
    test = Test.objects.get(id=test_id)

    if request.method == "POST":
        text = request.POST['text']
        option_a = request.POST['option_a']
        option_b = request.POST['option_b']
        option_c = request.POST['option_c']
        option_d = request.POST['option_d']
        correct_option=request.POST['correct_option']
        

        Question.objects.create(
            test=test,
            text=text,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            correct_option=correct_option
           
        )
        return redirect(f'/add-questions/{test.id}/')
    

    return render(request, 'add_questions.html', {'test': test})

@login_required
def view_questions(request, test_id):
    test = Test.objects.get(id=test_id)
    already_attempted = StudentAnswer.objects.filter(
        student=request.user,
        question__test=test
    ).exists()

    if already_attempted:
        
        messages.error(request, "You have already taken this test.")
        return redirect('/student/')
    
    
    questions = Question.objects.filter(test=test)

    return render(request, 'view_questions.html', {'test': test, 'questions': questions})



def delete_tests(request, test_id):
    Test.objects.get(id=test_id).delete()
    return redirect('teacher_page')



@login_required
def view_questions_2(request, test_id):
    test = Test.objects.get(id=test_id)
    already_attempted = StudentAnswer.objects.filter(
        student=request.user,
        question__test=test
    ).exists()

    if already_attempted:
        
        messages.error(request, "You have already taken this test.")
        return redirect('/student/')
    
    
    questions = Question.objects.filter(test=test)
    questions = Question.objects.filter(test=test)
    score=0
    total=questions.count()

    if request.method == 'POST':
        for question in questions:
            answer_key = f'answer_{question.id}'
            submitted_answer = request.POST.get(answer_key)
            

            if submitted_answer:
                StudentAnswer.objects.create(
                    student=request.user,
                    test=test,
                    question=question,
                    submitted_answer=submitted_answer.upper()
                )
            if submitted_answer==question.correct_option:
                score+=1
        return redirect(f'/student_result/{test.id}/{score}/{total}/')
        

    return render(request, 'view_questions(2).html', {'test': test, 'questions': questions})

@login_required
def student_answers_view(request):
    answers = StudentAnswer.objects.select_related('student', 'test', 'question')
    return render(request, 'student_answer.html', {'answers': answers})

@login_required
def student_result_view(request,test_id,score,total):
    test=Test.objects.get(id=test_id)
    return render(request,'student_result.html',{
        'score':score,'total':total,'test':test

    })
@login_required
def enter_test_code(request,test_id):
    test=Test.objects.get(id=test_id)
    if test.is_public:
        return redirect('view_questions(2)', test_id=test.id)
    if request.method=='POST':
        entered_code=request.POST.get('test_code')
        if entered_code==test.code:
             return redirect('view_questions(2)', test_id=test.id)
        else:
            messages.error(request, 'Incorrect  code.')
    return render(request, 'enter_test_code.html', {'test': test})

def logout_view(request):
    logout(request)
    return redirect('login_page')
       



