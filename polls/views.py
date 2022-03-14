from time import timezone

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.

# 사용자에게 보여지는 페이지 관리
from django.template import loader
from django.urls import reverse
from django.views import generic

from polls.models import Question, Choice

# ListView = 여러개의 객체를 보여주는 generic view
class IndexView(generic.ListView):
    template_name = 'polls/index.html' # 템플릿으로 사용할 html
    context_object_name = 'latest_question_list' # 템플릿에서 넘겨줄 때 사용할 변수 이름

    # 출력객체를 검색하기 위한 대상 QuerySet객체 또는 출력대상인 객체리스트를 반환 default = queryset속성값 반환
    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

# DetailView = 객체 하나에 대한 상세한 정보 보여주는 generic view
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    # get_object_or_404(장고모델, pk) = pk값에 해당하는 객체가 존재하면 반환 (아니면 404)
    # pk(primary key) = 모델에서 찍어낸 객체들을 구분해주는 값
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'question': question, 'error_message': "You didn't select a choice."})

    else :
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id)))
