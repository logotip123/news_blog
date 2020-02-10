from django.db import models
from django.utils.text import slugify

from users.models import CustomUser
from users.tasks import send_email

STATUS = (
    (1, "Approved"),
    (0, "Rejected")
)


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.author)

    def save(self, *args, **kwargs):
        if not self.id:
            send_email.delay(self.post.author.email, "New comment",
                             f"Тew comment for your news {self.post.title}:\n{self.content}")
        super().save(*args, **kwargs)