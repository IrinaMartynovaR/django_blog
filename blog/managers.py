from django.db.models import Manager, QuerySet
from django.utils import timezone

class PostQuerySet(QuerySet):
    def for_user(self, user=None):
        if user.is_staff:
            return self.all()
        else:
            return self.filter(published_date_lte=timezone.now())

class PostManager(Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def for_user(self, user=None):
        return self.get_queryset().for_user(user=user)

class PostPublishedManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            published_date__lte=timezone.now()
        )