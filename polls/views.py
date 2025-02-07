# from django.template import loader
from itertools import chain
from django.shortcuts import get_object_or_404, render
from .models import MultipleChoiceQuestion, TrueFalseQuestion
from django.db.models import F
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.shortcuts import get_object_or_404, render
from .models import Choice
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from .models import MultipleChoiceQuestion, TrueFalseQuestion, Choice
from django.db.models import QuerySet
from django.utils.text import slugify

class IndexView(generic.ListView):
    """Lists the latest 5 questions (both Multiple Choice & True/False)."""
    
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        multiple_choice_questions = list(
            MultipleChoiceQuestion.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
        )
        true_false_questions = list(
            TrueFalseQuestion.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
        )

        combined_questions = sorted(
            chain(multiple_choice_questions, true_false_questions),
            key=lambda q: q.pub_date,
            reverse=True
        )

        return combined_questions
 


class DetailView(generic.DetailView):
    template_name = "polls/detail.html"
    context_object_name = "question"

    def get_queryset(self):
        """Filter published questions dynamically."""
        return MultipleChoiceQuestion.objects.filter(pub_date__lte=timezone.now()) | TrueFalseQuestion.objects.filter(pub_date__lte=timezone.now())

    def get_object(self, queryset=None):
        """Fetch question based on request parameters."""
        question_id = self.kwargs["pk"]
        question_type = self.request.GET.get("question_type", "")

        if question_type == "Multiple Choice":
            question = get_object_or_404(MultipleChoiceQuestion, pk=question_id)
        elif question_type == "True/False":
            question = get_object_or_404(TrueFalseQuestion, pk=question_id)
        else:
            question = get_object_or_404(MultipleChoiceQuestion, pk=question_id)

        return question

    def get_context_data(self, **kwargs):
        """Pass question_type from URL params to the template."""
        context = super().get_context_data(**kwargs)
        context["question_type"] = self.request.GET.get("question_type", "")
        return context


class ResultsView(generic.DetailView):
    template_name = "polls/results.html"
    context_object_name = "question"

    def get_object(self):
        """Retrieve question based on question_id and question_type from URL params."""
        question_id = self.kwargs["pk"]
        question_type = self.request.GET.get("question_type", "")
        if question_type == "Multiple Choice":
            return get_object_or_404(MultipleChoiceQuestion, pk=question_id)
        elif question_type == "True/False":
            return get_object_or_404(TrueFalseQuestion, pk=question_id)
        else:
            return get_object_or_404(MultipleChoiceQuestion, pk=question_id)

    def get_context_data(self, **kwargs):
        """Pass question_type from URL params to the template."""
        context = super().get_context_data(**kwargs)
        context["question_type"] = self.request.GET.get("question_type", "")
        return context




def vote(request, question_id, question_type):
    """Handles voting for both Multiple Choice and True/False questions."""
    print("test")
    print(question_type)
    question_type = "True/False" if question_type == slugify("True/False") else "Multiple Choice"
    print(question_type)
    if question_type == "Multiple Choice":
        question = get_object_or_404(MultipleChoiceQuestion, pk=question_id)
        try:
            selected_choice = question.choices.get(pk=request.POST["choice"])
        except (KeyError, Choice.DoesNotExist):
            return render(
                request,
                "polls/detail.html",
                {
                    "question": question,
                    "error_message": "You didn't select a choice.",
                },
            )
        else:
            selected_choice.votes = F("votes") + 1
            selected_choice.save()

    elif question_type == "True/False":
        question = get_object_or_404(TrueFalseQuestion, pk=question_id)
        try:
            selected_answer = request.POST["answer"]
            is_correct = question.is_correct(selected_answer == "true")
        except KeyError:
            return render(
                request,
                "polls/detail.html",
                {
                    "question": question,
                    "error_message": "You didn't select an answer.",
                },
            )
        else:
            url = reverse("polls:results", args=(question.id,))
            return HttpResponseRedirect(f"{url}?question_type={question_type}")

    print(question)
    url = reverse("polls:results", args=(question.id,))
    return HttpResponseRedirect(f"{url}?question_type={question_type}")
