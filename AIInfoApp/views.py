from django.shortcuts import render, redirect
from .models import AiClass, AiStudents

# Create your views here.


def home(request):
    classes = AiClass.objects.all()

    context = {
        'classes': classes

    }

    return render(request, 'home.html', context)


def detail(request, class_pk):
    class_obj = AiClass.objects.get(pk=class_pk)
    student_obj = AiStudents.objects.filter(class_num=class_pk)

    context = {
        'class_pk': class_pk,
        'class_obj': class_obj,
        'student_obj': student_obj

    }

    return render(request, 'detail.html', context)


def add(request, class_pk):
    class_obj = AiClass.objects.get(pk=class_pk)
    if request.method == 'POST':
        AiStudents.objects.create(
            class_num=class_pk,
            name=request.POST['name'],
            phone_num=request.POST['phone_num'],
            intro_text=request.POST['intro_text']
        )
        return redirect('detail', class_pk)

    context = {
        'class_obj': class_obj,

    }

    return render(request, 'add.html', context)


def student(request, student_pk):

    student = AiStudents.objects.get(pk=student_pk)

    context = {
        'student': student
    }

    return render(request, 'student.html', context)


def edit(request, student_pk):
    if request.method == 'POST':
        target_student = AiStudents.objects.filter(pk=student_pk)

        target_student.update(
            name=request.POST['name'],
            phone_num=request.POST['phone_num'],
            intro_text=request.POST['intro_text']
        )
        return redirect('student', student_pk)

    student = AiStudents.objects.get(pk=student_pk)

    context = {
        'student': student
    }

    return render(request, 'edit.html', context)


def delete(request, student_pk):
    target_student = AiStudents.objects.get(pk=student_pk)
    target_student.delete()
    class_pk = target_student.class_num

    return redirect('detail', class_pk)
