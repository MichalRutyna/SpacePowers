from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import QuerySet
from django.urls.base import reverse


def get_user_nations(user) -> QuerySet:
    nations = user.ownerships.values_list('nation', flat=True)
    # convert ids to objects
    nations = Nation.objects.filter(id__in=nations)
    return nations


class Nation(models.Model):
    owners = models.ManyToManyField(User, through="Ownership")
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, verbose_name='nation_url', unique=True)
    active = models.BooleanField(default=False)

    banner = models.ImageField(null=True, blank=True, verbose_name='Banner', upload_to="banners/")
    flag = models.ImageField(null=True, blank=True, verbose_name='Flag', upload_to="flags/")
    coat_of_arms = models.ImageField(null=True, blank=True, verbose_name='Coat of Arms', upload_to="coats_of_arms/")

    population = models.PositiveIntegerField(default=0, blank=True, verbose_name='Population', validators=[MinValueValidator(1, message='Population must be greater than 0')])
    PKB = models.PositiveIntegerField(default=0, blank=True, verbose_name='PKB', validators=[MinValueValidator(1, message='PKB must be greater than 0')])

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

    def is_user_an_owner(self, user):
        return self.owners.contains(user)

    def get_title_of_user(self, user):
        return self.ownership_set.get(user=user).owner_title

    def get_details_url(self):
        return reverse("b:nation:details", kwargs={"slug": self.slug})

    def get_news_url(self):
        return reverse('b:news:nation', kwargs={"slug": self.slug})

    def log_info(self):
        return f"Nation {self.name}, owned by {self.owner}, population: {self.population}, PKB: {self.PKB}"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Nations"
        ordering = ['name']

class Ownership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ownerships')
    nation = models.ForeignKey(Nation, on_delete=models.CASCADE)
    owner_title = models.CharField(max_length=100, unique=False, null=False, default='glorious leader', verbose_name="Title")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "nation"], name="unique_ownership"
            )
        ]


class Army(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name', default="New army")
    nation = models.ForeignKey(Nation, on_delete=models.PROTECT, related_name='armies', verbose_name='allegiance')

    #location = models.ForeignKey()

    def get_upkeep(self) -> float:
        return 123.2

    def log_info(self):
        return f"Army {self.name} belonging to nation {self.nation}"
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "armies"
        ordering = ['name']



class Unit(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name', default="New unit")
    army = models.ForeignKey(Army, on_delete=models.PROTECT, related_name='units')

    size = models.IntegerField(default=0, verbose_name='Size')
    upkeep_per_unit = models.IntegerField(default=0, verbose_name='Upkeep per unit')


    def log_info(self):
        return f"Unit {self.name} belonging to army {self.army} ({self.army.nation}), size {self.size}, upkeep {self.upkeep_per_unit}"
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Units"
        ordering = ['name']