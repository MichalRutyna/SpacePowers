from django.db import models

from Nation.models import Nation


class Region(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name of the region")
    owner = models.ForeignKey(Nation, on_delete=models.PROTECT, related_name='regions', verbose_name="Who this region belongs to")

    region_type = models.CharField(max_length=100, default='planet', verbose_name="Type of region")
    slug = models.SlugField(max_length=100, unique=True)



    def log_info(self):
        return f"Region {self.name} belonging to nation {self.owner}, region type {self.region_type}"
    def __str__(self):
        return self.name