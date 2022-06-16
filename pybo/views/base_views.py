from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from ..models import Question, Answer
from django.db.models import Q, Count

def index(request):
    """
    pybo 목록 출력
    """
    # 입력 인자
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '') #검색어
    so = request.GET.get('so', 'recent') #정렬 기준

    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(
            num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else: # recent
        question_list = Question.objects.order_by('-create_date')

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) | #제목검색
            Q(content__icontains=kw) | #내용검색
            Q(author__username__icontains=kw) | #질문 글쓴이 검색
            Q(answer__author__username__icontains=kw) #답변 글쓴이 검색
        ).distinct()

    # 페이징 처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여 주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so} # page와 kw가 추가됨
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    """
    pybo 내용 출력
    """
    page = request.GET.get('page', '1') #답변 페이징을 위함
    so = request.GET.get('so', 'recent') 
    question = get_object_or_404(Question, pk=question_id)
    # question = Question.objects.get(id=question_id)

    """
    que_view_count = QuestionCount.objects.filter(ip=ip, question=question).count()

    if que_view_count == 0:
        que_count = QuestionCount(ip=ip, question=question)
        que_count.save()
        if question.view:
            question.view += 1
        else:
            question.view = 0
    question.save()
    """
    
    """
    답변을 추천순, 최신순으로 보여주기
    """
    if so == 'recommend': 
        answer_list = Answer.objects.filter(question=question).annotate(num_voter=Count('voter')).order_by('-num_voter','-create_date')
    else:
        answer_list = Answer.objects.filter(question=question).order_by('-create_date')

    paginator = Paginator(answer_list, 5) #답변을 5개까지만 보여주기
    page_obj = paginator.get_page(page)

    context = {'question': question, 'answer_list': page_obj, 'page': page, 'so': so}
    return render(request, 'pybo/question_detail.html', context)