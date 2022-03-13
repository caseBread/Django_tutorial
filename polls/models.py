import datetime
from django.utils import timezone
from django.db import models

# Create your models here.
# 데이터베이스 구조를 정의하는 곳

# 모델 변경 후
# >>> py manage.py makemigrations polls 해주어야 함
# 모델 변경 사실과 변경사항을 migration으로 저장시키고 싶다는 것을 django에게 알림

# py manage.py shell
# python shell 통해 django API를 활용할 수 있다.
# ex) django.utils



class Question(models.Model):

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now()

datetime.timedelta(days=1)

class Choice(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

