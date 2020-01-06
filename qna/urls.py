# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from qna import views as qna_views

urlpatterns = [
    url(r"^$", qna_views.IndexView.as_view(), name="index"),
    url(r"^ask/$", qna_views.AskView.as_view(), name="ask"),
    url(r"^question/(?P<slug>[-\w]+)/$",
        qna_views.QuestionAnswersView.as_view(),
        name="question"),
    url(r"^tag/(?P<tag_text>[-\w]+)/$",
        qna_views.TagView.as_view(),
        name="tag"),
    url(r"^vote/question/(?P<id>\d+)/$",
        qna_views.QuestionVoteView.as_view(), name="vote_question"),
    url(r"^vote/answer/(?P<id>\d+)/$",
        qna_views.AnswerVoteView.as_view(), name="vote_answer"),
    url(r"^mark/(?P<id>\d+)/$",
        qna_views.MarkAnswerView.as_view(), name="mark_answer"),
    url(r"^search/$",
        qna_views.SearchQuestionView.as_view(),
        name="search"),
]
