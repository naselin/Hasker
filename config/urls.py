"""hasker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from users import views as users_views
from qna import views as qna_views
from users.forms import LogInForm

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^$", qna_views.IndexView.as_view(), name="index"),
    url(r"^signup/$", users_views.SignUpView.as_view(), name="signup"),
    url(r"^settings/$",
        users_views.SettingsView.as_view(), name="settings"),
    url(r"^login/$", auth_views.login,
        {"template_name": "login.html", "authentication_form": LogInForm},
        name="login"),
    url(r"^logout/$", auth_views.logout,
        {"next_page": "login"},
        name="logout"),
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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
