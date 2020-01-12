# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import QuestionSerializer, AnswerSerializer, VoteSerializer
from .paginators import QuestionPagination, AnswerPagination
from qna.models import Tag, Question, Answer, Vote


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    pagination_class = QuestionPagination
    model = serializer_class.Meta.model
    queryset = model.objects.all().order_by("-post_time")


class BaseQuestionView (ListAPIView):
    serializer_class = QuestionSerializer
    pagination_class = QuestionPagination
    model = serializer_class.Meta.model


class TrendingView(BaseQuestionView):
    pagination_class = None

    def get_queryset(self):
        limit = settings.TRENDING_QUESTIONS
        return self.model.objects.all().order_by("-rating")[:limit]


class SearchView(BaseQuestionView):

    def get_queryset(self):
        search_text = ""
        if "q" in self.request.GET:
            search_text = self.request.GET.get("q")
            search_text = search_text.strip()
        if not search_text:
            return self.model.objects.none()
        queryset = self.model.objects.filter(Q(title__icontains=search_text) |
                                             Q(text__icontains=search_text))
        return queryset.order_by("-rating", "-post_time")


class TagView(BaseQuestionView):

    def get_queryset(self):
        tag_text = self.kwargs.get("tag_text")
        tag = Tag.objects.filter(tag_text=tag_text).first()
        if not tag:
            return self.model.objects.none()
        queryset = self.model.objects.filter(tags=tag)
        return queryset.order_by("-rating", "-post_time")


class QuestionAnswersView(ListAPIView):
    serializer_class = AnswerSerializer
    pagination_class = AnswerPagination
    model = serializer_class.Meta.model

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        question = get_object_or_404(Question, id=pk)
        queryset = self.model.objects.filter(question=question)
        return queryset.order_by("-rating", "-post_time")


class BaseVoteView(APIView):
    serializer_class = VoteSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    instance_type = None

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = request.user
        pk = self.kwargs.get("pk")
        vote_type = self.kwargs.get("vote")
        instance = get_object_or_404(self.instance_type, id=pk)
        rating = Vote.voting(user, instance, vote_type)
        return Response({"rating": rating}, status=status.HTTP_201_CREATED)


class QuestionVoteView(BaseVoteView):
    instance_type = Question


class AnswerVoteView(BaseVoteView):
    instance_type = Answer
