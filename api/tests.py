# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from datetime import timedelta

from django.test import TestCase
from django.db.models import Q
from django.shortcuts import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.conf import settings

from rest_framework import status
from rest_framework.test import APIClient

from qna.models import Tag, Question, Answer, Vote
from api.serializers import QuestionSerializer, AnswerSerializer

HaskerUser = get_user_model()


class QuestionViewSetTestCase(TestCase):
    questions = {
        "test1": {"text": "test1", "rating": 1, "days_ago": 0},
        "test2": {"text": "test2", "rating": 2, "days_ago": 1},
        "test3": {"text": "test3", "rating": 3, "days_ago": 2},
        "тест": {"text": "тест", "rating": 3, "days_ago": 3},
    }

    def setUp(self):
        self.author = HaskerUser.objects.create_user(
            username="User1", email="user1@selin.com.ru")
        for k, v in self.questions.items():
            title = k
            text = v["text"]
            rating = v["rating"]
            post_time = timezone.now() - timedelta(days=v["days_ago"])
            q = Question(title=title,
                         text=text,
                         rating=rating)
            q.save(author=self.author)
            q.post_time = post_time
            q.save()

    def test_questions_list(self):
        response = self.client.get("/api/questions/")
        questions = Question.objects.all().order_by(
            "-post_time")[:settings.QUESTIONS_PER_PAGE]
        serializer = QuestionSerializer(questions, many=True)
        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_question_details(self):
        question = Question.objects.filter(title="test1").first()
        pk = question.id
        serializer = QuestionSerializer(question)
        response = self.client.get("/api/questions/%d/" % pk)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_existant_question(self):
        pk = 1000000
        response = self.client.get("/api/questions/%d/" % pk)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TrendingViewTestCase(TestCase):
    questions = {
        "test1": {"text": "test1", "rating": 1, "days_ago": 0},
        "test2": {"text": "test2", "rating": 2, "days_ago": 1},
        "test3": {"text": "test3", "rating": 3, "days_ago": 2},
        "тест": {"text": "тест", "rating": 3, "days_ago": 3},
    }

    def setUp(self):
        self.author = HaskerUser.objects.create_user(
            username="User1", email="user1@selin.com.ru")
        for k, v in self.questions.items():
            title = k
            text = v["text"]
            rating = v["rating"]
            post_time = timezone.now() - timedelta(days=v["days_ago"])
            q = Question(title=title,
                         text=text,
                         rating=rating)
            q.save(author=self.author)
            q.post_time = post_time
            q.save()

    def test_trending_list(self):
        response = self.client.get("/api/questions/")
        questions = Question.objects.all().order_by(
            "-post_time")[:settings.QUESTIONS_PER_PAGE]
        serializer = QuestionSerializer(questions, many=True)
        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SearchViewTestCase(TestCase):
    questions = {
        "test1": {"text": "Qtst1", "rating": 1, "days_ago": 0, "tags": ("tag1",)},
        "test2": {"text": "Qtst2", "rating": 2, "days_ago": 1, "tags": ("tag2",)},
        "test3": {"text": "Qtst3", "rating": 3, "days_ago": 2, "tags": ("tag2", "tag3")},
        "тест": {"text": "Тест4", "rating": 3, "days_ago": 3, "tags": ("tag1", "tag3")},
    }

    def setUp(self):
        author = HaskerUser.objects.create_user(
            username="User1", email="user1@selin.com.ru")
        for k, v in self.questions.items():
            post_time = timezone.now() - timedelta(days=v["days_ago"])
            q = Question(title=k,
                         text=v["text"],
                         rating=v["rating"])
            q.save(author=author, tags=v["tags"])
            q.post_time = post_time
            q.save()

    def test_search_exact_title(self):
        title = "test1"
        response = self.client.get(reverse("api:search"), {"q": title})
        questions = Question.objects.filter(Q(title__icontains=title) |
                                            Q(text__icontains=title)).\
            order_by("-rating", "-post_time")
        serializer = QuestionSerializer(questions, many=True)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_view_mask_title(self):
        title = "test"
        response = self.client.get(reverse("api:search"), {"q": title})
        questions = Question.objects.filter(Q(title__icontains=title) |
                                            Q(text__icontains=title)).\
            order_by("-rating", "-post_time")
        serializer = QuestionSerializer(questions, many=True)
        self.assertEqual(len(response.data["results"]), 3)
        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_exact_text(self):
        text = "Qtst1"
        response = self.client.get(reverse("api:search"), {"q": text})
        questions = Question.objects.filter(Q(title__icontains=text) |
                                            Q(text__icontains=text)).\
            order_by("-rating", "-post_time")
        serializer = QuestionSerializer(questions, many=True)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_view_mask_text(self):
        text = "Qtst"
        response = self.client.get(reverse("api:search"), {"q": text})
        questions = Question.objects.filter(Q(title__icontains=text) |
                                            Q(text__icontains=text)).\
            order_by("-rating", "-post_time")
        serializer = QuestionSerializer(questions, many=True)
        self.assertEqual(len(response.data["results"]), 3)
        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TagViewTestCase(TestCase):
    questions = {
        "test1": {"text": "Qtst1", "rating": 1, "days_ago": 0, "tags": ("tag1",)},
        "test2": {"text": "Qtst2", "rating": 2, "days_ago": 1, "tags": ("tag2",)},
        "test3": {"text": "Qtst3", "rating": 3, "days_ago": 2, "tags": ("tag2", "tag3")},
        "тест": {"text": "Тест4", "rating": 3, "days_ago": 3, "tags": ("tag1", "tag3")},
    }

    def setUp(self):
        author = HaskerUser.objects.create_user(
            username="User1", email="user1@selin.com.ru")
        for k, v in self.questions.items():
            post_time = timezone.now() - timedelta(days=v["days_ago"])
            q = Question(title=k,
                         text=v["text"],
                         rating=v["rating"])
            q.save(author=author, tags=v["tags"])
            q.post_time = post_time
            q.save()

    def test_tag_list_existent_tag(self):
        tag_text = "tag3"
        tag = Tag.objects.filter(tag_text=tag_text).first()
        response = self.client.get(reverse("api:tag",
                                           kwargs={"tag_text": tag_text}))
        questions = Question.objects.filter(tags=tag).order_by(
            "-rating", "-post_time")
        serializer = QuestionSerializer(questions, many=True)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tag_list_non_existent_tag(self):
        tag_text = "tag123"
        tag = Tag.objects.filter(tag_text=tag_text).first()
        response = self.client.get(reverse("api:tag",
                                           kwargs={"tag_text": tag_text}))
        questions = Question.objects.filter(tags=tag).order_by(
            "-rating", "-post_time")
        serializer = QuestionSerializer(questions, many=True)
        self.assertEqual(len(response.data["results"]), 0)
        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class QuestionAnswersViewTestCase(TestCase):
    answers = {
        "test1": {"text": "test1", "rating": 1, "days_ago": 0, "author": "self.user1"},
        "test2": {"text": "test2", "rating": 2, "days_ago": 1, "author": "self.user2"},
        "test3": {"text": "test3", "rating": 3, "days_ago": 2, "author": "self.user1"},
        "test4": {"text": "test4", "rating": 3, "days_ago": 3, "author": "self.user2"},
    }

    def setUp(self):
        self.user1 = HaskerUser.objects.create_user(
            username="User1", email="user1@selin.com.ru")
        self.user2 = HaskerUser.objects.create_user(
            username="User2", email="user2@selin.com.ru")
        self.q = Question(title="Question", text="Test")
        self.q.save(author=self.user1)
        for k, v in self.answers.items():
            a = Answer(question=self.q,
                       text=v["text"],
                       rating=v["rating"],
                       author=eval(v["author"]))
            a.save()
            post_time = timezone.now() - timedelta(days=v["days_ago"])
            a.post_time = post_time
            a.save()
            self.q.post_answer(a)

    def test_question_answers_view(self):
        pk = self.q.id
        response = self.client.get(reverse("api:answers",
                                           kwargs={"pk": pk}))
        answers = Answer.objects.filter(
            question=self.q).order_by("-rating", "-post_time")
        serializer = AnswerSerializer(answers, many=True)
        self.assertEqual(len(response.data["results"]), 4)
        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_existent_question_answers_view(self):
        pk = 1000000
        response = self.client.get(reverse("api:answers",
                                           kwargs={"pk": pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ObtainTokenTestCase(TestCase):
    def setUp(self):
        self.user = HaskerUser.objects.create_user(
            username="User1",
            email="user1@selin.com.ru",
            password="correct_password"
        )

    def test_obtain_token_ok(self):
        response = self.client.post(
            reverse("api:token_obtain"),
            data=json.dumps(
                {"username": "User1", "password": "correct_password"}),
            content_type="application/json"
        )
        self.assertIsNotNone(response.data.get("token"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_obtain_token_nok(self):
        response = self.client.post(
            reverse("api:token_obtain"),
            data=json.dumps(
                {"username": "User1", "password": "incorrect_password"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(
            reverse("api:token_obtain"),
            data=json.dumps(
                {"username": "User2", "password": "correct_password"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class VotesViewsTestCase(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        self.q_author = HaskerUser.objects.create_user(
            username="User1",
            email="user1@selin.com.ru",
            password="correct_password")
        self.a_author = HaskerUser.objects.create_user(
            username="User2",
            email="user2@selin.com.ru",
            password="correct_password")
        self.q = Question(title="Question", text="Test")
        self.q.save(author=self.q_author)
        self.a = Answer(question=self.q, text="Answer", author=self.a_author)
        self.a.save()
        self.q.post_answer(self.a)
        response = self.client.post(
            reverse("api:token_obtain"),
            data=json.dumps(
                {"username": "User1", "password": "correct_password"}),
            content_type="application/json"
        )
        self.q_author_token = response.data.get("token")
        response = self.client.post(
            reverse("api:token_obtain"),
            data=json.dumps(
                {"username": "User2", "password": "correct_password"}),
            content_type="application/json"
        )
        self.a_author_token = response.data.get("token")

    def make_q_request(self, vote):
        return self.api_client.post(
            reverse("api:vote_question",
                    kwargs={"pk": self.q.pk, "vote": vote}),
            HTTP_AUTHORIZATION="jwt %s" % self.a_author_token
        )

    def make_a_request(self, vote):
        return self.api_client.post(
            reverse("api:vote_answer",
                    kwargs={"pk": self.a.pk, "vote": vote}),
            HTTP_AUTHORIZATION="jwt %s" % self.q_author_token
        )

    def test_question_vote_authorized_user(self):
        self.assertEqual(Question.objects.get(pk=self.q.pk).rating, 0)
        # UP
        response = self.make_q_request("up")
        self.assertEqual(Question.objects.get(pk=self.q.pk).rating, 1)
        self.assertEqual(response.data.get("rating"), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.make_q_request("up")
        self.assertEqual(Question.objects.get(pk=self.q.pk).rating, 1)
        self.assertEqual(response.data.get("rating"), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # DOWN
        response = self.make_q_request("down")
        self.assertEqual(Question.objects.get(pk=self.q.pk).rating, 0)
        self.assertEqual(response.data.get("rating"), 0)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.make_q_request("down")
        self.assertEqual(Question.objects.get(pk=self.q.pk).rating, -1)
        self.assertEqual(response.data.get("rating"), -1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.make_q_request("down")
        self.assertEqual(Question.objects.get(pk=self.q.pk).rating, -1)
        self.assertEqual(response.data.get("rating"), -1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_question_vote_not_authorized_user(self):
        response = self.client.post(
            reverse("api:vote_question",
                    kwargs={"pk": self.q.pk, "vote": "up"}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_answer_vote_authorized_user(self):
        self.assertEqual(Answer.objects.get(pk=self.a.pk).rating, 0)
        # UP
        response = self.make_a_request("up")
        self.assertEqual(Answer.objects.get(pk=self.a.pk).rating, 1)
        self.assertEqual(response.data.get("rating"), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.make_a_request("up")
        self.assertEqual(Answer.objects.get(pk=self.a.pk).rating, 1)
        self.assertEqual(response.data.get("rating"), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # DOWN
        response = self.make_a_request("down")
        self.assertEqual(Answer.objects.get(pk=self.a.pk).rating, 0)
        self.assertEqual(response.data.get("rating"), 0)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.make_a_request("down")
        self.assertEqual(Answer.objects.get(pk=self.a.pk).rating, -1)
        self.assertEqual(response.data.get("rating"), -1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.make_a_request("down")
        self.assertEqual(Answer.objects.get(pk=self.a.pk).rating, -1)
        self.assertEqual(response.data.get("rating"), -1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_answer_vote_not_authorized_user(self):
        response = self.client.post(
            reverse("api:vote_answer",
                    kwargs={"pk": self.a.pk, "vote": "up"}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
