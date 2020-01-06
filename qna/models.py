# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, transaction
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.contrib.auth import get_user_model


HaskerUser = get_user_model()


class Tag(models.Model):
    tag_text = models.CharField(max_length=30, blank=False, null=False)

    def __unicode__(self):
        return self.tag_text


class Question(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    text = models.TextField(blank=False, null=False)
    author = models.ForeignKey(
        HaskerUser, related_name="questions")
    post_time = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name="questions")
    slug = models.SlugField(max_length=200, unique=True)
    num_answers = models.PositiveIntegerField(default=0)
    correct_answer = models.OneToOneField("Answer", default=None, null=True,
                                          related_name="correct_answer")
    rating = models.IntegerField(default=0)
    votes = GenericRelation("Vote", related_query_name="questions")

    def save(self, author=None, tags=None, *args, **kwargs):
        if author:
            self.author = author
            self.slug = slugify(self.title, allow_unicode=True)
            # @TODO: Check it in form validation.
            existent_slug = Question.objects.filter(slug=self.slug)
            if existent_slug:
                while existent_slug:
                    self.slug = "%s-%s" % (self.slug, "1")
                    existent_slug = Question.objects.filter(slug=self.slug)
        super(Question, self).save(*args, **kwargs)
        if tags:
            for word in tags:
                try:
                    tag = Tag.objects.get(tag_text=word)
                except Tag.DoesNotExist:
                    tag = Tag(tag_text=word)
                    tag.save()
                self.tags.add(tag)

    @transaction.atomic()
    def post_answer(self, answer):
        self.num_answers += 1
        self.save()
        answer.question = self
        answer.save()

    def mark_answer(self, a):
        if self.correct_answer == a:
            self.correct_answer = None
        else:
            self.correct_answer = a
        self.save()

    def send_email_notify(self, request, answer):
        mailto = self.author.email
        subject = "User %s posted a new answer for your question '%s'." % (
            answer.author.username, self.title)
        message = "%s\nVisit <a href='%s'> and read it." % (
            subject, request.build_absolute_uri())
        send_mail(
            subject,
            message,
            "nikita@selin.com.ru",
            [mailto],
            fail_silently=True,
        )

    def __unicode__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question)
    text = models.TextField(blank=False, null=False)
    author = models.ForeignKey(
        HaskerUser, related_name="answers")
    post_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    votes = GenericRelation("Vote", related_query_name="answers")

    def __unicode__(self):
        return "%s - %s" % (self.question.title, self.text)


class Vote(models.Model):
    UP_VOTE = "U"
    DOWN_VOTE = "D"
    ACTIVITY_TYPES = (
        (UP_VOTE, "Up Vote"),
        (DOWN_VOTE, "Down Vote"),
    )

    user = models.ForeignKey(HaskerUser)
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    @staticmethod
    @transaction.atomic()
    def voting(user, instance, vote_type):
        rating = instance.rating
        try:
            vote = instance.votes.get(user=user)
        except ObjectDoesNotExist:
            vote = None
        if vote_type == "up":
            if vote:
                if vote.activity_type == "D":
                    vote.delete()
                    rating += 1
            else:
                instance.votes.create(activity_type="U", user=user)
                rating += 1
        elif vote_type == "down":
            if vote:
                if vote.activity_type == "U":
                    vote.delete()
                    rating -= 1
            else:
                instance.votes.create(activity_type="D", user=user)
                rating -= 1
        else:
            raise ValueError
        instance.rating = rating
        instance.save()
        return rating
