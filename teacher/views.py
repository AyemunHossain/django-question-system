from django.shortcuts import render,redirect,reverse

import exam
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from exam import models as QMODEL
from exam import forms as QFORM
from django.contrib.auth.models import User
from django import forms as djangoForms


#for showing signup/login button for teacher
def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'teacher/teacherclick.html')


@login_required(login_url='login/google-oauth2')
def teacher_dashboard_view(request):
    dict={
    'total_course':QMODEL.Course.objects.filter(invitedExamineEmail__icontains=(request.user.email)).count(),
    # 'total_question':QMODEL.Question.objects.all().count(),
    }
    return render(request,'teacher/teacher_dashboard.html',context=dict)

@login_required(login_url='login/google-oauth2')
def teacher_exam_view(request):
    return render(request,'teacher/teacher_exam.html')


@login_required(login_url='login/google-oauth2')
def teacher_add_exam_view(request):
    courseForm=QFORM.CourseForm()
    if request.method=='POST':
        courseForm=QFORM.CourseForm(request.POST)
        if courseForm.is_valid():      
            course = courseForm.save()
            course.add_by_id = request.user.id
            course.save()

        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-view-exam')
    return render(request,'teacher/teacher_add_exam.html',{'courseForm':courseForm})

@login_required(login_url='login/google-oauth2')
def teacher_view_exam_view(request):
    courses = QMODEL.Course.objects.filter(add_by_id= request.user.id)
    return render(request,'teacher/teacher_view_exam.html',{'courses':courses})

@login_required(login_url='login/google-oauth2')
def delete_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/teacher/teacher-view-exam')

@login_required(login_url='login/google-oauth2')
def teacher_question_view(request):
    return render(request,'teacher/teacher_question.html')

@login_required(login_url='login/google-oauth2')
def teacher_add_question_view(request):
    questionForm=QFORM.QuestionForm()
    questionForm.fields['courseID'] = djangoForms.ModelChoiceField(queryset=QMODEL.Course.objects.filter(isViva=False, add_by_id = request.user.id),empty_label="Course Name", to_field_name="id")
    
    if request.method=='POST':
        questionForm=QFORM.QuestionForm(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            course=QMODEL.Course.objects.get(id=request.POST.get('courseID'))
            question.course=course
            question.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-view-question')
    return render(request,'teacher/teacher_add_question.html',{'questionForm':questionForm})



@login_required(login_url='login/google-oauth2')
def teacher_add_viva_view(request):
    vivaForm=QFORM.VivaForm()
    vivaForm.fields['courseID'] = djangoForms.ModelChoiceField(queryset=QMODEL.Course.objects.filter(isViva=True, add_by_id = request.user.id),empty_label="Course Name", to_field_name="id")
    
    if request.method=='POST':
        vivaForm=QFORM.VivaForm(request.POST)
        if vivaForm.is_valid():
            vaiva=vivaForm.save(commit=False)
            course=QMODEL.Course.objects.get(id=request.POST.get('courseID'))
            vaiva.course=course
            vaiva.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-view-question')
    return render(request,'teacher/teacher_add_viva.html',{'vivaForm':vivaForm})


@login_required(login_url='login/google-oauth2')
def teacher_view_viva_view(request):
    courses= QMODEL.Course.objects.filter(isViva=True,add_by_id=request.user.id)
    return render(request,'teacher/teacher_view_viva.html',{'courses':courses})

@login_required(login_url='login/google-oauth2')
def teacher_view_question_view(request):
    courses= QMODEL.Course.objects.filter(isViva=False,add_by_id=request.user.id)
    return render(request,'teacher/teacher_view_question.html',{'courses':courses})

@login_required(login_url='login/google-oauth2')
def see_question_view(request,pk):
    questions=QMODEL.Question.objects.all().filter(course_id=pk)
    return render(request,'teacher/see_question.html',{'questions':questions})

@login_required(login_url='login/google-oauth2')
def see_viva_question_view(request,pk):
    questions=QMODEL.Viva.objects.all().filter(course_id=pk)
    return render(request,'teacher/see_vaiva_question.html',{'questions':questions})


@login_required(login_url='login/google-oauth2')
def remove_question_view(request,pk):
    question=QMODEL.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/teacher/teacher-view-question')


@login_required(login_url='login/google-oauth2')
def student_exam_view(request):
    courses=QMODEL.Course.objects.filter(invitedExamineEmail__icontains=(request.user.email),isViva=False)
    return render(request,'teacher/student_exam.html',{'courses':courses})

@login_required(login_url='login/google-oauth2')
def student_viva_exam_view(request):
    courses=QMODEL.Course.objects.filter(invitedExamineEmail__icontains=(request.user.email),isViva=True)
    return render(request,'teacher/student_viva_exam.html',{'courses':courses})

@login_required(login_url='login/google-oauth2')
def take_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    total_questions=QMODEL.Question.objects.all().filter(course=course).count()
    questions=QMODEL.Question.objects.all().filter(course=course)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    
    return render(request,'teacher/take_exam.html',{'course':course,'total_questions':total_questions,'total_marks':total_marks})

@login_required(login_url='login/google-oauth2')
def start_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    questions=QMODEL.Question.objects.filter(course_id=course.id)


    if(len(questions)>0):
        if request.method=='POST':
            pass
        response= render(request,'teacher/start_exam.html',{'course':course,'questions':questions,'questionNo':len(questions)})
        response.set_cookie('course_id',course.id)
        return response
    else:
        response= render(request,'teacher/start_exam.html',{'course':course,'questions':[],'questionNo':0})
        response.set_cookie('course_id',course.id)
        return response


@login_required(login_url='login/google-oauth2')
def start_viva_exam_view(request,pk):
    vivaForm=QFORM.VivaForm2()
    Viva=QMODEL.Viva.objects.filter(course_id=pk)[0]
    course = QMODEL.Course.objects.get(id=pk)
    student = User.objects.get(id=request.user.id)
    if request.method=='POST':
        vivaForm=QFORM.VivaForm2(request.POST)
        
        if vivaForm.is_valid():
            result = QMODEL.VivaResult()
            result.answer_link = vivaForm.cleaned_data['answer_link']
            result.exam=course
            result.student=student
            result.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/')
    return render(request,'teacher/start_viva_exam.html',{'vivaForm':vivaForm,'viva':Viva})


@login_required(login_url='login/google-oauth2')
def teacher_evaluate_viva_view(request):
    result = QMODEL.VivaResult.objects.filter(exam__add_by=request.user).select_related('student')
    return render(request,'teacher/teacher_evaluate_viva.html',{'result':result or []})

@login_required(login_url='login/google-oauth2')
def evaluate_viva_exam_view(request,pk):
    vivaResultForm=QFORM.VivaResultForm()
    vivaResult=QMODEL.VivaResult.objects.filter(pk=pk)[0]
    viva = QMODEL.Viva.objects.filter(id=vivaResult.exam.id)[0]
    print(vivaResult)

    
    if request.method=='POST':
        vivaResultForm=QFORM.VivaResultForm (request.POST)
        
        if vivaResultForm.is_valid():
            vivaResult.marks = vivaResultForm.cleaned_data['marks']
            vivaResult.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-evaluate-viva')
    return render(request,'teacher/start_viva_evaluate.html',{'vivaForm':vivaResultForm, 'vivaResult':vivaResult,'viva':viva})

@login_required(login_url='login/google-oauth2')
def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course=QMODEL.Course.objects.get(id=course_id)
        
        total_marks=0
        questions=QMODEL.Question.objects.all().filter(course=course)
        for i in range(len(questions)):
            
            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        student = User.objects.get(id=request.user.id)
        result = QMODEL.Result()
        result.marks=total_marks
        result.exam=course
        result.student=student
        result.save()

        return HttpResponseRedirect('view-result')



@login_required(login_url='login/google-oauth2')
def view_result_view(request):
    courses=QMODEL.Course.objects.filter(isViva=False,invitedExamineEmail__icontains=(request.user.email))
    return render(request,'teacher/view_result.html',{'courses':courses})   

@login_required(login_url='login/google-oauth2')
def check_marks_view(request,pk):
    
    course=QMODEL.Course.objects.get(id=pk)
    student = User.objects.get(id=request.user.id)
    try:
        results= QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    except:
        results = []
    return render(request,'teacher/check_marks.html',{'results':results})

@login_required(login_url='login/google-oauth2')
def check_viva_marks_view(request,pk):
    
    course=QMODEL.Course.objects.get(id=pk)
    student = User.objects.get(id=request.user.id)
    try:
        results= QMODEL.VivaResult.objects.all().filter(exam=course).filter(student=student)
    except:
        results = []
    return render(request,'teacher/check_marks.html',{'results':results})

@login_required(login_url='login/google-oauth2')
def student_marks_view(request):
    courses=QMODEL.Course.objects.filter(isViva=False,invitedExamineEmail__icontains=(request.user.email))
    vaiva = QMODEL.Course.objects.filter(isViva=True,invitedExamineEmail__icontains=(request.user.email))
    return render(request,'teacher/student_marks.html',{'courses':courses,'viva':vaiva})
  