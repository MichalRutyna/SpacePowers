from django.contrib.auth.models import User
from django.db import models
from django.urls.base import reverse


class Nation(models.Model):
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='claimed_nations')
    owner_title = models.CharField(max_length=100, unique=False, null=False, default='glorious leader')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, verbose_name='nation_url', unique=True)
    active = models.BooleanField(default=False)

    population = models.IntegerField(default=0, verbose_name='Population')
    PKB = models.IntegerField(default=0, verbose_name='PKB')

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


class Army(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    nation = models.ForeignKey(Nation, on_delete=models.PROTECT, related_name='armies', verbose_name='allegiance')

    #location = models.ForeignKey()

    def get_upkeep(self) -> float:
        return 123.2

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "armies"
        ordering = ['name']



class Unit(models.Model):
    name = models.CharField(max_length=100)
    army = models.ForeignKey(Army, on_delete=models.PROTECT, related_name='units')

    size = models.IntegerField()
    upkeep_per_unit = models.IntegerField()



    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Units"
        ordering = ['name']