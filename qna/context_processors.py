from django.conf import settings

from .models import Question


def trending_list(request):
    queryset = Question.objects.all().order_by("-rating")
    limit = settings.TRENDING_QUESTIONS
    return {
        "trending_list": queryset[:limit]
    }
