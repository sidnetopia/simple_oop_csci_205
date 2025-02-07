import datetime
from django.db import models
from django.utils import timezone

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class BaseQuestion(TimestampedModel):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    class Meta:
        abstract = True

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    @classmethod
    def total_questions(cls):
        return cls.objects.count()

    def get_question_type(self):
        raise NotImplementedError("Subclasses must implement get_question_type()")


class MultipleChoiceQuestion(BaseQuestion):
    def get_choices(self):
        return self.choices.all()

    def has_choices(self):
        return self.choices.exists()


    def get_question_type(self):
        return "Multiple Choice"


class Choice(models.Model):
    question = models.ForeignKey(
        MultipleChoiceQuestion, on_delete=models.CASCADE, related_name="choices"
    )
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    def add_vote(self):
        self.votes += 1
        self.save()

    @classmethod
    def total_votes(cls):
        return cls.objects.aggregate(total=models.Sum("votes"))["total"] or 0
    
    
class TrueFalseQuestion(BaseQuestion):
    answer = models.BooleanField(default=True)

    def is_correct(self, selected_answer):
        return self.answer == selected_answer
    
    def get_question_type(self):
        return "True/False"

class QuestionFactory:
    """Factory to create different types of questions"""

    @staticmethod
    def create_question(question_type, question_text, pub_date=timezone.now()):
        if question_type == "MCQ":
            return MultipleChoiceQuestion(question_text=question_text, pub_date=pub_date)
        elif question_type == "TF":
            return TrueFalseQuestion(question_text=question_text, pub_date=pub_date)
        else:
            raise ValueError("Invalid question type")
