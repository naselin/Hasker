# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.views import View
from django.views.generic import CreateView, ListView
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Q
from django.conf import settings

from .models import Question, Tag, Answer, Vote
from .forms import AskForm, AnswerForm


class IndexView(ListView):
    model = Question
    context_object_name = "questions"
    template_name = "index.html"
    paginate_by = settings.QUESTIONS_PER_PAGE

    def get_ordering(self):
        order_by = self.request.GET.get("order", "post_time")
        if order_by == "rating":
            return ["-rating", "-post_time"]
        return ["-post_time", "-rating"]

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["page"] = self.request.GET.get("page", 1)
        context["order"] = self.request.GET.get("order", "post_time")
        return context

    def get_queryset(self):
        queryset = super(IndexView, self).get_queryset()
        return queryset


class AskView(LoginRequiredMixin, CreateView):
    login_url = "login"
    redirect_field_name = "next"
    model = Question
    context_object_name = "question"
    template_name = "ask.html"
    form_class = AskForm

    @transaction.atomic()
    def form_valid(self, form):
        question = form.save(commit=False)
        question.save(self.request.user, form.cleaned_data.get("tags"))
        return redirect(reverse("question",
                                kwargs={"slug": question.slug}))


class QuestionAnswersView(ListView):
    model = Answer
    context_object_name = "answers"
    template_name = "question.html"
    form = AnswerForm
    paginate_by = settings.ANSWERS_PER_PAGE

    def get_context_data(self, **kwargs):
        context = super(QuestionAnswersView, self).get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        question = get_object_or_404(Question, slug=slug)
        form = self.form()
        context["question"] = question
        context["form"] = form
        return context

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        question = get_object_or_404(Question, slug=slug)
        queryset = Answer.objects.filter(question=question)
        return queryset.order_by("-rating", "-post_time")

    def post(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        question = get_object_or_404(Question, slug=slug)
        form = self.form(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            question.post_answer(answer)
            question.send_email_notify(request, answer)
            return redirect(reverse("question", kwargs={"slug": slug}))
        context = {
            "form": form
        }
        return render(request, self.template_name, context)


class TagView(ListView):
    model = Question
    context_object_name = "questions"
    template_name = "tag.html"
    paginate_by = settings.QUESTIONS_PER_PAGE

    def get_context_data(self, **kwargs):
        context = super(TagView, self).get_context_data(**kwargs)
        tag_text = self.kwargs.get("tag_text")
        context["tag_text"] = tag_text
        return context

    def get_queryset(self):
        tag_text = self.kwargs.get("tag_text")
        tag = Tag.objects.filter(tag_text=tag_text).first()
        if not tag:
            return Question.objects.none()
        queryset = super(TagView, self).get_queryset()
        return queryset.filter(tags=tag).order_by("-rating", "-post_time")


class SearchQuestionView(ListView):
    model = Question
    context_object_name = "questions"
    template_name = "search.html"
    paginate_by = settings.QUESTIONS_PER_PAGE

    def get(self, request, *args, **kwargs):
        search_text = ""
        if "q" in self.request.GET:
            search_text = self.request.GET.get("q")
            search_text = search_text.strip()
        if search_text.startswith("tag:"):
            tag_text = search_text[len("tag:"):]
            return redirect(reverse("tag", kwargs={"tag_text": tag_text}))
        self.object_list = self.get_queryset(search_text)
        context = super(SearchQuestionView, self).get_context_data(**kwargs)
        context["page"] = self.request.GET.get("page", 1)
        context["q"] = self.request.GET.get("q", "")
        return render(request, self.template_name, context=context)

    def get_queryset(self, search_text):
        if not search_text:
            return Question.objects.none()
        queryset = super(SearchQuestionView, self).get_queryset()
        queryset = queryset.filter(Q(title__icontains=search_text) |
                                   Q(text__icontains=search_text))
        return queryset.order_by("-rating", "-post_time")


class QuestionVoteView(View):
    instance_type = Question

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            if user == AnonymousUser():
                raise PermissionDenied("Authorized user required.")
        except AttributeError:
            raise PermissionDenied("Invalid request.")
        iid = self.kwargs.get("id")
        vote_type = request.POST["vote"]
        instance = get_object_or_404(self.instance_type, id=iid)
        rating = Vote.voting(user, instance, vote_type)
        return JsonResponse({"rating": rating})


class AnswerVoteView(QuestionVoteView):
    instance_type = Answer


class MarkAnswerView(View):
    def post(self, request, *args, **kwargs):
        try:
            user = request.user
        except AttributeError:
            raise PermissionDenied("Invalid request.")
        a_id = self.kwargs.get("id")
        a = get_object_or_404(Answer, id=a_id)
        q = a.question
        if q.author != user:
            raise PermissionDenied("Question author required.")
        try:
            q.mark_answer(a)
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=500)
