from django.db import models
from django.utils import timezone


class Test(models.Model):
    name = models.TextField()
    type = models.TextField()
    questions = models.IntegerField(null=True)
    published = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Question(models.Model):
    number = models.IntegerField(default=1)
    question = models.TextField()
    option_one = models.TextField()
    option_two = models.TextField()
    option_three = models.TextField()
    option_four = models.TextField()
    option_five = models.TextField()
    correct_answer = models.TextField()
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.question
