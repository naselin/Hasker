from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from .views import QuestionViewSet, TrendingView, SearchView, TagView,\
    QuestionAnswersView, QuestionVoteView, AnswerVoteView

router = routers.DefaultRouter()
router.register(r"questions", QuestionViewSet)
app_name = "api"

urlpatterns = [
    url(r"^", include(router.urls)),
    url(r"^login/$", obtain_jwt_token, name="token_obtain"),
    url(r"^trending/$", TrendingView.as_view(), name="trending"),
    url(r"^search/$", SearchView.as_view(), name="search"),
    url(r"^tag/(?P<tag_text>[-\w]+)/$", TagView.as_view(), name="tag"),
    url(r"^questions/(?P<pk>[\d]+)/answers/$",
        QuestionAnswersView.as_view(), name="answers"),
    url(r"^vote/question/(?P<pk>\d+)/(?P<vote>[-\w]+)/$",
        QuestionVoteView.as_view(), name="vote_question"),
    url(r"^vote/answer/(?P<pk>\d+)/(?P<vote>[-\w]+)/$",
        AnswerVoteView.as_view(), name="vote_answer"),
]
