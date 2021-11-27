from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from app.forms import CustomUserCreationForm
from app.models import Test, Question, CustomUser


def home(request):
    return render(request, 'index.html', locals())


def services(request):
    return render(request, 'services.html', locals())


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        user = form.save()
        login(request, user)
        return redirect("login")
    form = CustomUserCreationForm()
    return render(request, 'register.html', locals())


def login_user(request):
    print(request.user)
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password1')
        if CustomUser.objects.filter(email=email).exists():
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('dashboard_admin')
                else:
                    return redirect('dashboard')
            else:
                print('not a user')

    return render(request, 'login.html', locals())


def logout_view(request):
    if request.user is not None:
        logout(request)
        return redirect('home')
    HttpResponse(request)


def check_email(request):
    email = request.POST.get('email')
    data = {
        "is_taken": CustomUser.objects.filter(email=email).exists()
    }
    return JsonResponse(data)


def dashboard(request):
    print(request.user.ga_client_id)
    return render(request, 'dashboard/index.html', locals())


@user_passes_test(lambda u: u.is_superuser)
def admin(request):
    return render(request, 'admin/index.html', locals())


@user_passes_test(lambda u: u.is_superuser)
def upload_nmc(request):
    published_tests = Test.objects.filter(published=True).order_by('-created_on')
    unpublished_tests = Test.objects.filter(published=False).order_by('-created_on')
    return render(request, 'admin/upload_nmc.html', locals())


@user_passes_test(lambda u: u.is_superuser)
def create_test(request):
    name = request.POST.get('name')
    test_type = request.POST.get('test_type')
    questions = request.POST.get('questions')
    test = Test.objects.create(name=name, type=test_type, questions=questions)
    test.save()
    data = {
        "created": Test.objects.filter(id=test.id).exists(),
        "test_id": test.id,
        "test_questions": test.questions
    }
    return JsonResponse(data)


@user_passes_test(lambda u: u.is_superuser)
def delete_test(request):
    test_id = request.POST.get('test_id')
    test = Test.objects.get(id=test_id)
    test.delete()
    data = {
        "deleted": True
    }
    return JsonResponse(data)


@user_passes_test(lambda u: u.is_superuser)
def create_question(request):
    question = request.POST.get('question')
    option_one = request.POST.get('option_one')
    option_two = request.POST.get('option_two')
    option_three = request.POST.get('option_three')
    option_four = request.POST.get('option_four')
    option_five = request.POST.get('option_five')
    correct_answer = request.POST.get('correct_answer')
    test_id = request.POST.get('test_id')

    test = Test.objects.get(id=test_id)
    if not Question.objects.filter(test=test).exists():
        number = 1
    else:
        max = 0
        for q in Question.objects.all():
            if q.number > max:
                max = q.number
        number = max + 1
    new_question = Question.objects.create(number=number, question=question, option_one=option_one,
                                           option_two=option_two,
                                           option_three=option_three, option_four=option_four, option_five=option_five,
                                           correct_answer=correct_answer, test=test)
    new_question.save()
    data = {"test": "success", "question": new_question.id}
    return JsonResponse(data)


@user_passes_test(lambda u: u.is_superuser)
def view_test(request, id):
    test = Test.objects.get(id=id)
    questions = Question.objects.filter(test=test).order_by('created_on')
    if request.method == 'POST' and 'question_id' in request.POST:
        question = Question.objects.get(id=request.POST.get('question_id'))
        number_to_shift = question.number
        question.delete()
        for q in Question.objects.filter(test=test):
            if q.number > number_to_shift:
                q.number = q.number - 1
                q.save()
        test.questions = test.questions - 1
        test.save()
        return HttpResponseRedirect(request.path_info)
    if request.method == 'POST' and 'publish_test' in request.POST:
        test.published = True
        test.save()
        return HttpResponseRedirect(request.path_info)
    if request.method == 'POST' and 'unpublish_test' in request.POST:
        test.published = False
        test.save()
        return HttpResponseRedirect(request.path_info)
    if request.method == 'POST' and 'question' in request.POST:
        question = request.POST.get('question')
        option_one = request.POST.get('option_one')
        option_two = request.POST.get('option_two')
        option_three = request.POST.get('option_three')
        option_four = request.POST.get('option_four')
        option_five = request.POST.get('option_five')
        correct_answer = request.POST.get('correct_answer')
        if not Question.objects.filter(test=test).exists():
            number = 1
        else:
            max = 0
            for q in Question.objects.all():
                if q.number > max:
                    max = q.number
            number = max + 1
        new_question = Question.objects.create(number=number, question=question, option_one=option_one,
                                               option_two=option_two,
                                               option_three=option_three, option_four=option_four,
                                               option_five=option_five,
                                               correct_answer=correct_answer, test=test)
        new_question.save()
        test.questions = test.questions + 1
        test.save()
        return HttpResponseRedirect(request.path_info)
    return render(request, 'admin/view_test.html', locals())


@user_passes_test(lambda u: u.is_superuser)
def edit_question(request, id):
    question = Question.objects.get(id=id)
    if request.method == 'POST':
        question.question = request.POST.get('question')
        question.option_one = request.POST.get('option_one')
        question.option_two = request.POST.get('option_two')
        question.option_three = request.POST.get('option_three')
        question.option_four = request.POST.get('option_four')
        question.option_five = request.POST.get('option_five')
        question.correct_answer = request.POST.get('correct_answer')
        question.save()
        return redirect('view_test', question.test.id)
    return render(request, 'admin/edit_question.html', locals())


def nmc_practice_questions(request):
    published_tests = Test.objects.filter(published=True).order_by('-created_on')
    return render(request, 'dashboard/nmc_practice_questions.html', locals())


def take_test(request, id):
    test = Test.objects.get(id=id)
    questions = Question.objects.filter(test=test).order_by('created_on')
    return render(request, 'dashboard/take_test.html', locals())


def update_ga_client_id(request):
    user=request.user
    if user.ga_client_id == '' or user.ga_client_id is None:
        user.ga_client_id = request.POST.get('ga_client_id')
        user.save()
        data = {
            "updated": True
        }
    elif user.ga_client_id == request.POST.get('ga_client_id'):

        data = {
            "exists": False
        }
    return JsonResponse(data)
