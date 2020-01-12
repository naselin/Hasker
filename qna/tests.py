# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from datetime import timedelta

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import reverse
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

from .models import Tag, Question, Answer, Vote
from .views import QuestionVoteView, AnswerVoteView, MarkAnswerView

HaskerUser = get_user_model()


class ModelsTestCase(TestCase):
    def setUp(self):
        self.user1 = HaskerUser.objects.create(
            username="User1", email="user1@selin.com.ru")
        self.user2 = HaskerUser.objects.create(
            username="User2", email="user2@selin.com.ru")
        for tag in ("tag1", "tag2", "tag3"):
            Tag.objects.create(tag_text=tag)

    def test_save_question(self):
        tags = Tag.objects.all()
        q_title = "Test question."
        q_text = "Test text."
        q_new = Question(title=q_title, text=q_text)
        q_new.save(author=self.user1, tags=tags)
        q_saved = Question.objects.filter(title=q_title).first()
        self.assertIsNotNone(q_saved)
        self.assertEqual(q_saved.author, self.user1)
        self.assertEqual(q_saved.title, q_title)
        self.assertEqual(q_saved.text, q_text)
        self.assertSetEqual(tags, q_saved.tags.all())

    def test_save_answer(self):
        q = Question.objects.create(author=self.user1)
        a_text = "Test answer."
        a_new = Answer(text=a_text, author=self.user2)
        self.assertEqual(q.num_answers, 0)
        q.post_answer(a_new)
        self.assertEqual(q.num_answers, 1)
        a_saved = Answer.objects.filter(text=a_text).first()
        self.assertIsNotNone(a_saved)
        self.assertEqual(a_saved.question, q)

    def test_mark_answer(self):
        q = Question.objects.create(author=self.user1)
        a1 = Answer.objects.create(author=self.user2, question=q)
        a2 = Answer.objects.create(author=self.user2, question=q)
        self.assertIsNone(q.correct_answer)
        q.mark_answer(a1)
        self.assertEqual(q.correct_answer, a1)
        q.mark_answer(a2)
        self.assertEqual(q.correct_answer, a2)

    def test_unmark_answer(self):
        q = Question.objects.create(author=self.user1)
        a = Answer.objects.create(author=self.user2, question=q)
        q.mark_answer(a)
        self.assertEqual(q.correct_answer, a)
        q.mark_answer(a)
        self.assertIsNone(q.correct_answer)

    def test_question_votes(self):
        q = Question.objects.create(author=self.user1)
        with self.assertRaises(ValueError):
            Vote.voting(self.user2, q, "invalid_vote_type")
        self.assertEqual(q.rating, 0)
        Vote.voting(self.user2, q, "up")
        self.assertEqual(q.rating, 1)
        Vote.voting(self.user2, q, "up")
        self.assertEqual(q.rating, 1)
        Vote.voting(self.user2, q, "down")
        self.assertEqual(q.rating, 0)
        Vote.voting(self.user2, q, "down")
        self.assertEqual(q.rating, -1)
        Vote.voting(self.user2, q, "down")
        self.assertEqual(q.rating, -1)

    def test_answer_votes(self):
        q = Question.objects.create(author=self.user1)
        a = Answer.objects.create(author=self.user2, question=q)
        with self.assertRaises(ValueError):
            Vote.voting(self.user1, a, "invalid_vote_type")
        self.assertEqual(a.rating, 0)
        Vote.voting(self.user1, a, "down")
        self.assertEqual(a.rating, -1)
        Vote.voting(self.user1, a, "down")
        self.assertEqual(a.rating, -1)
        Vote.voting(self.user1, a, "up")
        self.assertEqual(a.rating, 0)
        Vote.voting(self.user1, a, "up")
        self.assertEqual(a.rating, 1)
        Vote.voting(self.user1, a, "up")
        self.assertEqual(a.rating, 1)


class IndexViewTestCase(TestCase):
    questions = {
        "test1": {"text": "test1", "rating": 1, "days_ago": 0},
        "test2": {"text": "test2", "rating": 2, "days_ago": 1},
        "test3": {"text": "test3", "rating": 3, "days_ago": 2},
        "тест": {"text": "тест", "rating": 3, "days_ago": 3},
    }

    def setUp(self):
        self.author = HaskerUser.objects.create(
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

    def test_index_view_default_sort(self):
        ql = ["test1", "test2", "test3", "тест"]
        response = self.client.get(reverse("index"))
        context_ql = response.context["questions"]
        for i in range(len(ql)):
            self.assertEqual(context_ql[i].title, ql[i])
            self.assertEqual(context_ql[i].author, self.author)

    def test_index_view_rating_sort(self):
        ql = ["test3", "тест", "test2", "test1"]
        response = self.client.get(reverse("index"), {"order": "rating"})
        context_ql = response.context["questions"]
        for i in range(len(ql)):
            self.assertEqual(context_ql[i].title, ql[i])

    def test_trending_list(self):
        ql = ["test3", "тест", "test2", "test1"]
        response = self.client.get(reverse("index"))
        context_cl = response.context["trending_list"]
        for i in range(len(ql)):
            self.assertEqual(context_cl[i].title, ql[i])


class QuestionAnswersViewTestCase(TestCase):
    answers = {
        "test1": {"text": "test1", "rating": 1, "days_ago": 0, "author": "self.user1"},
        "test2": {"text": "test2", "rating": 2, "days_ago": 1, "author": "self.user2"},
        "test3": {"text": "test3", "rating": 3, "days_ago": 2, "author": "self.user1"},
        "test4": {"text": "test4", "rating": 3, "days_ago": 3, "author": "self.user2"},
    }

    def setUp(self):
        self.user1 = HaskerUser.objects.create(
            username="User1", email="user1@selin.com.ru")
        self.user2 = HaskerUser.objects.create(
            username="User2", email="user2@selin.com.ru")
        q = Question(title="Question", text="Test")
        q.save(author=self.user1)
        for k, v in self.answers.items():
            a = Answer(question=q,
                       text=v["text"],
                       rating=v["rating"],
                       author=eval(v["author"]))
            a.save()
            post_time = timezone.now() - timedelta(days=v["days_ago"])
            a.post_time = post_time
            a.save()
            q.post_answer(a)

    def test_question_answers_view(self):
        response = self.client.get(reverse("question",
                                           kwargs={"slug": "question"}))
        al = ["test3", "test4", "test2", "test1"]
        context_q = response.context["question"]
        self.assertEqual(context_q.author, self.user1)
        context_al = response.context["answers"]
        for i in range(len(al)):
            self.assertEqual(context_al[i].text, al[i])
            self.assertEqual(context_al[i].author,
                             eval(self.answers[al[i]]["author"]))


class SearchViewTestCase(TestCase):
    questions = {
        "test1": {"text": "Qtst1", "rating": 1, "days_ago": 0, "tags": ("tag1",)},
        "test2": {"text": "Qtst2", "rating": 2, "days_ago": 1, "tags": ("tag2",)},
        "test3": {"text": "Qtst3", "rating": 3, "days_ago": 2, "tags": ("tag2", "tag3")},
        "тест": {"text": "Тест4", "rating": 3, "days_ago": 3, "tags": ("tag1", "tag3")},
    }

    def setUp(self):
        author = HaskerUser.objects.create(
            username="User1", email="user1@selin.com.ru")
        for k, v in self.questions.items():
            post_time = timezone.now() - timedelta(days=v["days_ago"])
            q = Question(title=k,
                         text=v["text"],
                         rating=v["rating"])
            q.save(author=author, tags=v["tags"])
            q.post_time = post_time
            q.save()

    def test_search_view_exact_title(self):
        title = "test1"
        response = self.client.get("/search/", {"q": title})
        found = response.context["questions"][0]
        self.assertEqual(found.title, title)

    def test_search_view_mask_title(self):
        ql = ["test3", "test2", "test1"]
        title = "test"
        response = self.client.get("/search/", {"q": title})
        found = response.context["questions"]
        for i in range(len(ql)):
            self.assertEqual(found[i].title, ql[i])

    def test_search_view_exact_text(self):
        text = "Qtst1"
        response = self.client.get("/search/", {"q": text})
        q = response.context["questions"][0]
        self.assertEqual(q.text, text)

    def test_search_view_mask_text(self):
        ql = ["Qtst3", "Qtst2", "Qtst1"]
        text = "Qtst"
        response = self.client.get("/search/", {"q": text})
        found = response.context["questions"]
        for i in range(len(ql)):
            self.assertEqual(found[i].text, ql[i])

    def test_search_view_tag(self):
        tag = "tag:tag3"
        tag_url = "/tag/tag3/"
        ql = ["test3", "тест"]
        response = self.client.get("/search/", {"q": tag})
        self.assertEqual(response.url, tag_url)
        redir_response = self.client.get(response.url)
        found = redir_response.context["questions"]
        for i in range(len(ql)):
            self.assertEqual(found[i].title, ql[i])


class VotesViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = HaskerUser.objects.create(
            username="User1", email="user1@selin.com.ru")
        self.user2 = HaskerUser.objects.create(
            username="User2", email="user2@selin.com.ru")
        self.q = Question(title="Question", text="Test")
        self.q.save(author=self.user1)
        self.a = Answer(question=self.q, text="Answer", author=self.user2)
        self.a.save()
        self.q.post_answer(self.a)

    def make_q_request(self, post_data, user):
        request = self.factory.post(reverse("vote_question",
                                            kwargs={"id": self.q.id}),
                                    data=post_data)
        request.user = user
        return QuestionVoteView.as_view()(request, id=self.q.id)

    def make_a_request(self, post_data, user):
        request = self.factory.post(reverse("vote_answer",
                                            kwargs={"id": self.a.id}),
                                    data=post_data)
        request.user = user
        return AnswerVoteView.as_view()(request, id=self.a.id)

    def make_m_request(self, user):
        request = self.factory.post(reverse("mark_answer",
                                            kwargs={"id": self.a.id}))
        request.user = user
        return MarkAnswerView.as_view()(request, id=self.a.id)

    def test_question_vote_authorized_user(self):
        user = self.user2
        expected_rating = 1
        post_data = {
            "vote": "up",
        }
        response = self.make_q_request(post_data, user)
        self.assertEqual(json.loads(response.content)["rating"],
                         expected_rating)
        response = self.make_q_request(post_data, user)
        self.assertEqual(json.loads(response.content)["rating"],
                         expected_rating)
        expected_rating = 0
        post_data = {
            "vote": "down",
        }
        response = self.make_q_request(post_data, user)
        self.assertEqual(json.loads(response.content)["rating"],
                         expected_rating)
        expected_rating = -1
        response = response = self.make_q_request(post_data, user)
        self.assertEqual(json.loads(response.content)["rating"],
                         expected_rating)
        response = self.make_q_request(post_data, user)
        self.assertEqual(json.loads(response.content)["rating"],
                         expected_rating)

    def test_question_vote_not_authorized_user(self):
        post_data = {
            "vote": "up",
        }
        user = AnonymousUser()
        with self.assertRaises(PermissionDenied):
            self.make_q_request(post_data, user)

    def test_answer_vote_authorized_user(self):
        user = self.user1
        expected_rating = 1
        post_data = {
            "vote": "up",
        }
        response = self.make_a_request(post_data, user)
        self.assertEqual(json.loads(response.content)["rating"],
                         expected_rating)
        response = self.make_a_request(post_data, user)
        self.assertEqual(json.loads(response.content)["rating"],
                         expected_rating)
        expected_rating = 0
        post_data = {
            "vote": "down",
        }
        response = self.make_a_request(post_data, user)
        self.assertEqual(json.loads(response.content)["rating"],
                         expected_rating)
        expected_rating = -1
        response = response = self.make_a_request(post_data, user)
        self.assertEqual(json.loads(response.content)["rating"],
                         expected_rating)
        response = self.make_a_request(post_data, user)
        self.assertEqual(json.loads(response.content)["rating"],
                         expected_rating)

    def test_answer_vote_not_authorized_user(self):
        post_data = {
            "vote": "up",
        }
        with self.assertRaises(PermissionDenied):
            self.make_a_request(post_data, AnonymousUser())

    def test_mark_answer_user_is_question_author(self):
        response = self.make_m_request(self.user1)
        self.assertEqual(response.status_code, 200)

    def test_mark_answer_user_is_not_question_author(self):
        with self.assertRaises(PermissionDenied):
            self.make_m_request(AnonymousUser())
        with self.assertRaises(PermissionDenied):
            self.make_m_request(self.user2)
