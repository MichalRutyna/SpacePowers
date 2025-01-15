from django.contrib.auth.models import User
from django.db import models

class Nation(models.Model):
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    population = models.IntegerField()
    PKB = models.IntegerField()

    def get_name_foreign(self):
        return "Our friends" + self.name

    # if foreign nations should see some changed info it is modified here
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

    def __str__(self):
        return self.name

    objects = models.Manager()

    class Meta:
        verbose_name_plural = "Nations"
        ordering = ['name']
