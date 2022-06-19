from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    has_answer = models.BooleanField(default=True) #답변 가능 여부

    def __str__(self):
        return self.name

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    modify_date = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField()
    voter = models.ManyToManyField(User, related_name='voter_question')  # voter 추가
    view = models.PositiveIntegerField(default=0, blank=True, null=True)
    #카테고리 모델 연결하기
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_question')

    def __str__(self):
        return self.subject

class QuestionCount(models.Model): #조회수 모델
    ip = models.CharField(max_length=30)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    def __unicode__(self): #ip 유니코드로 반환
        return self.ip

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    modify_date = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField()
    voter = models.ManyToManyField(User, related_name='voter_answer')  # voter 추가

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)


