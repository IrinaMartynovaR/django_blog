from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from .managers import PostManager, PostPublishedManager


class Post(models.Model):

    published = PostPublishedManager()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()

    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    objects = PostManager()

    def post_detail(request, id):
        post = get_object_or_404(Post, id=id)
        if not post.is_publish() and not request.user.is_staff:
            raise Http404('Запись в блоге не найдена')
        return render(request, 'blog/post_detail.html',{'post': post})

    def is_publish(self):
        return True if self.published_date else False

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    class Meta:
        verbose_name ='Запись в блоге'
        verbose_name_plural = 'Запись в блоге'

    def __str__(self):
        return self.title