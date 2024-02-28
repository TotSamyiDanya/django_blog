from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='avatars/')


class Post(models.Model):
    title = models.TextField()
    subtitle = models.TextField()
    topic = models.TextField()
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    cover = models.ImageField(upload_to='covers/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def likes(self):
        return Like.objects.filter(post_id=self.pk).count()

    @property
    def comments(self):
        return Comment.objects.filter(post_id=self.pk).count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


class Poll(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)


class Question(models.Model):
    poll = models.ForeignKey(Poll, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)


class PollComplete(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
