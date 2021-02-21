from typing import List
from django.http import HttpResponse
from .models import Question
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .forms import QuestionForm
from .forms import QuestionForm, AnswerForm


def index(request):
    """
    pybo 목록 출력
    """
    # 함수로 빼면 테스트코드 짜기 좋고 controller단 코드가 단순해져서 코드 읽기가 편해집니다 :)
    # question_list = Question.objects.order_by('-create_date')
    question: List = get_questions()
    context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)
    return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")

def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    question = Question.objects.get(id=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

def answer_create(request, question_id):
    """
    pybo 답변등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


def question_create(request):
    """
    pybo 질문등록
    """
    if request.method == 'POST':
        # Vaildation 역할도 수행합니다. 
        # 라이브러리를 사용하지 않는다면 is_valid_question_create(request.POST)
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)
