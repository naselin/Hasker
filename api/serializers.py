from rest_framework import serializers

from qna.models import Question, Answer


class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.CharField(
        read_only=True, source="author.username")
    post_time = serializers.DateTimeField(
        read_only=True, format='%Y-%m-%d %H:%M:%S')
    tags = serializers.StringRelatedField(
        read_only=True, many=True)

    class Meta:
        model = Question
        fields = ("id", "title", "text", "author", "post_time",
                  "tags", "num_answers", "correct_answer", "rating")


class AnswerSerializer(serializers.ModelSerializer):
    author = serializers.CharField(
        read_only=True, source="author.username")
    post_time = serializers.DateTimeField(
        read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Answer
        fields = ("id", "text", "author", "post_time", "rating")


class VoteSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField()
