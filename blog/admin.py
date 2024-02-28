from django.contrib import admin
from .models import User, Post, Comment, Like, Poll, Question, Choice, Vote, PollComplete


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = User


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Meta:
        model = Post


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    class Meta:
        model = Like


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    class Meta:
        model = Comment


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionInline(admin.TabularInline):
    model = Question
    inlines = [
        ChoiceInline
    ]
    extra = 1


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    inlines = [
        QuestionInline
    ]

    class Meta:
        model = Poll


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        ChoiceInline
    ]

    class Meta:
        model = Question


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    class Meta:
        model = Choice


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    class Meta:
        model = Vote


@admin.register(PollComplete)
class PollComplete(admin.ModelAdmin):
    class Meta:
        model = PollComplete
