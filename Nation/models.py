from django.contrib.auth.models import User
from django.db import models
from django.urls.base import reverse


class Nation(models.Model):
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='claimed_nations')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, verbose_name='nation_url', unique=True)
    active = models.BooleanField(default=True)
    population = models.IntegerField()
    PKB = models.IntegerField()

    def get_name_foreign(self):
        # proof of concept for accessing data from other nations
        return "Our friends" + self.name

    # if foreign nations should see some changed info, then it is modified here
    def get_data_as_foreign_nation(self):
        response = {}
        for field in self._meta.get_fields():
            if field.name == 'id':
                continue
            if field.name == 'owner':
                response[field.name] = User.objects.get(pk=field.value_from_object(self))
            else:
                response[field.name] = field.value_to_string(self)
        return response

    def get_news_url(self):
        return reverse('b:news:nation', kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Nations"
        ordering = ['name']
