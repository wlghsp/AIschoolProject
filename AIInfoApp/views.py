from django.shortcuts import render, redirect
from .models import AiClass, AiStudent, StudentPost
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
ERROR_MSG = {
    'ID_EXIST': '이미 사용 중인 아이디 입니다.',
    'ID_NOT_EXIST': '존재하지 않는 아이디 입니다.',
    'ID_PW_MISSING': '아이디와 비밀번호를 다시 확인해주세요.',
    'PW_CHECK': '비밀번호가 일치하지 않습니다.',

}


def home(request):
    classes = AiClass.objects.all()

    context = {
        'classes': classes

    }

    return render(request, 'home.html', context)


def detail(request, class_pk):
    # class_pk에 해당하는 반을 가져온다
    # (그 반에 속해 있는 학생은 foreign key로 연결되어 있다)
    class_obj = AiClass.objects.get(pk=class_pk)

    context = {
        'class_obj': class_obj
    }

    return render(request, 'detail.html', context)


def add(request, student_pk):
    student = AiStudent.objects.get(pk=student_pk)
    if request.method == 'POST':
        StudentPost.objects.create(
            intro=request.POST['intro'],
            writer=student
        )
        return redirect('student', student_pk)

    return render(request, 'add.html')


def student(request, student_pk):

    student = AiStudent.objects.get(pk=student_pk)

    context = {
        'student': student
    }

    return render(request, 'student.html', context)


def edit(request, student_pk):
    if request.method == 'POST':
        target_student = AiStudent.objects.filter(pk=student_pk)

        target_student.update(
            name=request.POST['name'],
            phone_num=request.POST['phone_num'],
        )
        return redirect('student', student_pk)

    student = AiStudent.objects.get(pk=student_pk)

    context = {
        'student': student
    }

    return render(request, 'edit.html', context)


def delete(request, student_pk):
    target_student = AiStudent.objects.get(pk=student_pk)
    target_student.delete()
    class_pk = target_student.class_num

    return redirect('detail', class_pk)


def signup(request):

    context = {
        'error': {
            'state': False,
            'msg': ''
        },
    }
    if request.method == 'POST':

        user_id = request.POST['user_id']
        user_pw = request.POST['user_pw']
        user_pw_check = request.POST['user_pw_check']

        name = request.POST['name']
        phone_num = request.POST['phone_num']
        class_num = request.POST['class_num']

        participate_class = AiClass.objects.get(class_num=class_num)

        user = User.objects.filter(username=user_id)

        if (user_id and user_pw):
            # 존재하지 않는 아이디라면
            if len(user) == 0:
                if (user_pw == user_pw_check):

                    created_user = User.objects.create_user(
                        username=user_id,
                        password=user_pw
                    )
                    auth.login(request, created_user)

                    AiStudent.objects.create(
                        participate_class=participate_class,
                        user=created_user,
                        name=name,
                        phone_num=phone_num
                    )

                    return redirect('home')
                else:
                    context['error']['state'] = True
                    context['error']['msg'] = ERROR_MSG['PW_CHECK']
            else:
                context['error']['state'] = True
                context['error']['msg'] = ERROR_MSG['ID_EXIST']
        else:
            context['error']['state'] = True
            context['error']['msg'] = ERROR_MSG['ID_PW_MISSING']
    return render(request, 'signup.html', context)


def login(request):

    context = {
        'error': {
            'state': False,
            'msg': ''
        },
    }
    if request.method == 'POST':

        user_id = request.POST['user_id']
        user_pw = request.POST['user_pw']

        user = User.objects.filter(username=user_id)

        if (user_id and user_pw):
            if len(user) != 0:

                user = auth.authenticate(
                    username=user_id,
                    password=user_pw
                )
                if user != None:
                    auth.login(request, user)

                    return redirect('home')
                else:
                    context['error']['state'] = True
                    context['error']['msg'] = ERROR_MSG['PW_CHECK']
            else:
                context['error']['state'] = True
                context['error']['msg'] = ERROR_MSG['ID_NOT_EXIST']
        else:
            context['error']['state'] = True
            context['error']['msg'] = ERROR_MSG['ID_PW_MISSING']
    return render(request, 'login.html', context)


def logout(request):
    auth.logout(request)
    return redirect('home')
