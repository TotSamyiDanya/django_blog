import json

from django.views import View
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Post, User, Like, Comment, Poll, Question, Choice, Vote, PollComplete
from .forms import LoginForm, RegisterForm, PostForm


def home(request):
    query = request.GET.get('query')
    posts = get_posts(query) or []
    if 'name' in request.COOKIES:
        user = User.objects.get(name=request.COOKIES['name'])
        likes = [current_like.post for current_like in Like.objects.filter(user=user) or []]
        response = render(
            request,
            'home.html',
            {
                'posts': posts,
                'user': user,
                'likes': likes
            }
        )
        return response
    else:
        register_form = RegisterForm()
        login_form = LoginForm()
        response = render(
            request,
            'home.html',
            {
                'posts': posts,
                'register_form': register_form,
                'login_form': login_form
            }
        )
        return response


def post(request, post_id):
    current_post = Post.objects.get(id=post_id)
    current_post.date = parse_date(current_post.date)
    paragraphs = current_post.content.split('\r\n\r\n')
    comments = Comment.objects.filter(post=current_post) or []
    for current_comment in comments:
        current_comment.date = parse_date(current_comment.date)
    if 'name' in request.COOKIES:
        user = User.objects.get(name=request.COOKIES['name'])
        like_exists = Like.objects.filter(post=current_post, user=user).exists()
        if like_exists:
            current_like = Like.objects.get(post=current_post, user=user)
        else:
            current_like = None
        response = render(
            request,
            'post.html',
            {
                'post': current_post,
                'paragraphs': paragraphs,
                'comments': comments,
                'user': user,
                'like': current_like,
            }
        )
        return response
    else:
        register_form = RegisterForm()
        login_form = LoginForm()
        response = render(
            request,
            'post.html',
            {
                'post': current_post,
                'paragraphs': paragraphs,
                'comments': comments,
                'register_form': register_form,
                'login_form': login_form,
            }
        )
        return response


def editor(request, post_id=None):
    user = User.objects.get(name=request.COOKIES['name'])
    post_form = PostForm()
    if post_id is None:
        response = render(
            request,
            'editor.html',
            {
                'post_form': post_form,
                'user': user,
                'mode': 'create'
            }
        )
        return response
    else:
        current_post = Post.objects.get(id=post_id)
        data = {
            'title': current_post.title,
            'subtitle': current_post.subtitle,
            'topic': current_post.topic,
            'content': current_post.content,
        }
        post_form = PostForm(initial=data)
        response = render(
            request,
            'editor.html',
            {
                'post_form': post_form,
                'user': user,
                'mode': 'update',
                'image': current_post.cover.url,
                'post_id': post_id
            }
        )
        return response


def personal(request):
    user = User.objects.get(name=request.COOKIES['name'])
    posts = Post.objects.filter(user=user) or []
    likes = [current_like.post for current_like in Like.objects.filter(user=user) or []]
    for current_post in posts:
        current_post.date = parse_date(current_post.date)
    response = render(
        request,
        'personal.html',
        {
            'posts': posts,
            'user': user,
            'likes': likes
        }
    )
    return response


def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            data = register_form.cleaned_data
            user = User(
                name=data['name'],
                password=data['password'],
                avatar=data['avatar']
            )
            user.save()
            response = redirect('home')
            return response
        else:
            response = redirect('home')
            return response
    else:
        response = redirect('home')
        return response


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            data = login_form.cleaned_data
            if check_user(data['name'], data['password']):
                response = redirect('home')
                response.set_cookie('name', data['name'])
                return response
            else:
                response = redirect('home')
                return response
        else:
            response = redirect('home')
            return response


def logout(request):
    response = redirect('home')
    response.delete_cookie('name')
    response.delete_cookie('csrftoken')
    return response


def like(request):
    if request.method == 'POST':
        current_post = Post.objects.get(id=request.POST.get('post_id'))
        user = User.objects.get(name=request.POST.get('user_name'))
        like_exists = Like.objects.filter(post=current_post, user=user)
        if like_exists:
            current_like = Like.objects.get(post=current_post, user=user)
            current_like.delete()
            response = JsonResponse({'message': 'deleted'})
            return response
        else:
            current_like = Like(post=current_post, user=user)
            current_like.save()
            response = JsonResponse({'message': 'created'})
            return response


def comment(request):
    if request.method == 'POST':
        current_post = Post.objects.get(id=request.POST.get('post_id'))
        user = User.objects.get(name=request.POST.get('user_name'))
        content = request.POST.get('content')
        current_comment = Comment(
            post=current_post,
            user=user,
            content=content
        )
        current_comment.save()
        referer = request.META['HTTP_REFERER']
        response = redirect(referer)
        return response


def create(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            data = post_form.cleaned_data
            current_post = Post(
                title=data['title'],
                subtitle=data['subtitle'],
                topic=data['topic'],
                content=data['content'],
                cover=data['cover'],
                user=User.objects.get(name=request.COOKIES['name'])
            )
            current_post.save()
            response = redirect('home')
            return response
        else:
            referer = request.META['HTTP_REFERER']
            response = redirect(referer)
            return response
    else:
        referer = request.META['HTTP_REFERER']
        response = redirect(referer)
        return response


def update(request):
    if request.method == 'POST':
        current_post = Post.objects.get(id=request.POST.get('post_id'))
        current_post.title = request.POST.get('title')
        current_post.subtitle = request.POST.get('subtitle')
        current_post.topic = request.POST.get('topic')
        current_post.content = request.POST.get('content')
        current_post.cover = request.FILES.get('cover')
        current_post.save()
        response = redirect('post', post_id=request.POST.get('post_id'))
        return response


def delete(request):
    current_post = Post.objects.get(id=request.GET.get('post_id'))
    user = User.objects.get(name=request.COOKIES['name'])
    if current_post.user == user:
        current_post.delete()
        response = redirect('personal')
        return response


class PollClass(View):
    @staticmethod
    def get(request):
        user = User.objects.get(name=request.COOKIES['name'])
        current_poll = Poll.objects.get(id=6)
        poll_completed = PollComplete.objects.filter(user=user, poll=current_poll).exists()
        questions = Question.objects.filter(poll=current_poll)
        choices = {}
        for current_question in questions:
            current_question_choices = Choice.objects.filter(question=current_question)
            choices[current_question.id] = current_question_choices

        user_votes = {}

        for current_question in questions:
            user_choices = Choice.objects.filter(question=current_question)
            for choice in user_choices:
                user_has_voted = Vote.objects.filter(choice=choice, user=user).exists()
                if user_has_voted:
                    user_votes[current_question.id] = choice.id

        return render(request, 'poll.html', context={
            'hide_menu': True,
            'poll_id': current_poll.id,
            'user': user,
            'questions': questions,
            'choices': choices,
            'completed': poll_completed,
            'user_votes': user_votes
        })

    @staticmethod
    def post(request):
        current_choice = Choice.objects.get(id=request.POST.get('choice_id'))
        current_question = Question.objects.get(id=request.POST.get('question_id'))
        user = User.objects.get(name=request.POST.get('user_name'))

        choices = Choice.objects.filter(question=current_question)
        for choice in choices:
            user_has_voted = Vote.objects.filter(choice=choice, user=user).exists()
            if user_has_voted:
                current_vote = Vote.objects.filter(choice=choice, user=user)
                current_vote.delete()

        current_vote = Vote(choice=current_choice, user=user)
        current_vote.save()

        choices = Choice.objects.filter(question=current_question)
        votes_count = 0
        percents = {}
        for choice in choices:
            votes_count = votes_count + Vote.objects.filter(choice=choice).count()

        for choice in choices:
            votes = Vote.objects.filter(choice=choice).count()
            percents[choice.id] = round((votes / votes_count) * 100) if votes_count else 0

        data = json.dumps(percents)

        response = JsonResponse(data, safe=False)
        return response


def complete_poll(request):
    if request.method == 'POST':
        user = User.objects.get(name=request.COOKIES['name'])
        current_poll = Poll.objects.get(id=request.POST.get('poll_id'))
        poll_complete = PollComplete(user=user, poll=current_poll)
        poll_complete.save()
        response = JsonResponse({'message': 'created'})
        return response



def get_posts(query):
    posts = []
    if query is not None:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(topic__icontains=query) |
            Q(user__name__icontains=query)
        ) or []
    else:
        posts = Post.objects.all() or []
    for current_post in posts:
        current_post.date = parse_date(current_post.date)
    return posts


def parse_date(date):
    current_date = timezone.now()
    difference = current_date - date
    if difference.days >= 365:
        return f"{difference.days // 365} г"
    elif difference.days >= 1:
        return f"{difference.days} д"
    elif difference.seconds >= 3600:
        return f"{difference.seconds // 3600} ч"
    elif difference.seconds >= 60:
        return f"{difference.seconds // 60} мин"
    else:
        return f"{difference.seconds} сек"


def check_user(name, password):
    user_exists = User.objects.filter(name=name).exists()
    if user_exists:
        user = User.objects.get(name=name)
        if user.password == password:
            return True
        else:
            return False
    else:
        return False
