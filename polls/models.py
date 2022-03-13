from django.db import models

# Create your models here.
# 데이터베이스 구조를 정의하는 곳

# 모델 변경 후
# >>> py manage.py makemigrations polls 해주어야 함
# 모델 변경 사실과 변경사항을 migration으로 저장시키고 싶다는 것을 django에게 알림

class Question(models.Model):

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

