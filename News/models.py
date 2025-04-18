from django.contrib.auth.models import User
from django.db import models
from django.db.models.query_utils import Q
from django.urls import reverse
from martor.models import MartorField

from Nation.models import Nation
from managers import NewsManager


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, verbose_name='Category_url', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('b:news:category', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Category(s)'
        verbose_name_plural = 'Categories'
        ordering = ['title']


class Arc(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, verbose_name='Slug', unique=True)
    users = models.ManyToManyField(User, verbose_name='Users')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('b:news:arc', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Arc(s)'
        verbose_name_plural = 'Arcs'
        ordering = ['title']


class Tag(models.Model):
    title = models.CharField(max_length=50)
    success_roll_required = models.BooleanField(default=False, verbose_name='Success roll required')
    secrecy_roll_required = models.BooleanField(default=False, verbose_name='Secrecy roll required')
    slug = models.SlugField(max_length=50, verbose_name='Slug url', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('b:news:tag', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['title']


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Link')
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=True, verbose_name='Author')
    nation = models.ForeignKey(Nation, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Nation')
    content = MartorField(blank=True, verbose_name='Content')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Published')

    edited_at = models.DateTimeField(auto_now=True, verbose_name='Edited')
    edited = models.BooleanField(default=False, verbose_name='Was edited')

    update_subscribe = models.ManyToManyField(User, blank=True, verbose_name='Subscribed', related_name='subscribed_post')

    views = models.IntegerField(default=0, verbose_name='Number of views')
    seen_by = models.ManyToManyField(User, blank=True, verbose_name='Seen by', related_name='+')
    liked_by = models.ManyToManyField(User, blank=True, verbose_name='Liked by', related_name='liked_posts')

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts', verbose_name='Category')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name='Tags')
    arcs = models.ManyToManyField(Arc, blank=True, related_name='posts', verbose_name='Arcs')

    # overrides
    success_roll_override = models.BooleanField(null=True, blank=True, verbose_name='Success roll override')
    secrecy_roll_override = models.BooleanField(null=True, blank=True, verbose_name='Secrecy roll override')
    published_override = models.BooleanField(null=True, blank=True, verbose_name='Published override')

    published_by_user = models.BooleanField(default=False, verbose_name='Published by user')
    approved_by_admin = models.BooleanField(default=False, verbose_name='Approved by admin')

    active = models.BooleanField(default=True, verbose_name='Active')

    objects = models.Manager()
    active_posts = NewsManager()

    @property
    def is_published(self):
        if self.published_override is not None:
            return self.published_override
        if self.has_unrolled_rolls():
            return False
        if self.has_unrolled_rolls():
            return False
        if not self.approved_by_admin:
            return False
        if not self.published_by_user:
            return False
        return True

    @property
    def likes(self):
        return self.liked_by.count()

    def is_liked_by(self, user):
        return self.liked_by.filter(id=user).exists()

    def is_user_an_author(self, user):
        return self.author == user

    def requires_success_roll(self):
        if self.success_roll_override is not None:
            return self.success_roll_override
        return self.tags.filter(success_roll_required=True).exists()

    def requires_secrecy_roll(self):
        if self.secrecy_roll_override is not None:
            return self.secrecy_roll_override
        return self.tags.filter(secrecy_roll_required=True).exists()

    def get_success_rolls(self):
        return self.rolls.filter(roll_type=Roll.RollTypes.SUCCESS)

    def get_secrecy_rolls(self):
        return self.rolls.filter(roll_type=Roll.RollTypes.SECRECY)

    def has_unrolled_rolls(self):
        return self.rolls.filter(roll=None).exists()

    def has_rolls_without_description(self):
        return self.rolls.filter(Q(roll_description__isnull=True) | Q(roll_description="")).exists()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('b:news:post', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Post(s)'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']

class Roll(models.Model):

    class RollTypes(models.TextChoices):
        SUCCESS = 'success', "Success"
        SECRECY = 'secrecy', "Secrecy"

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='rolls', related_query_name="rolls", verbose_name='Post')
    roll = models.IntegerField(null=True, blank=True, verbose_name='Roll value')
    roll_description = models.TextField(null=True, blank=True, verbose_name='Roll description')
    roll_type = models.CharField(max_length=255, choices=RollTypes.choices, default=RollTypes.SUCCESS, verbose_name='Roll type')




class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', related_query_name='comments', verbose_name='Post')
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=True, verbose_name='Author')
    nation = models.ForeignKey(Nation, on_delete=models.PROTECT, null=True, verbose_name='Nation')

    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    edited_at = models.DateTimeField(auto_now=True, verbose_name='Edited')
    edited = models.BooleanField(default=False, verbose_name='Is edited')

    liked_by = models.ManyToManyField(User, blank=True, verbose_name='Liked by', related_name='liked_comments')

    is_published = models.BooleanField(default=True, verbose_name='Is published')
    metagame = models.BooleanField(default=False, verbose_name='Metagame')

    active = models.BooleanField(default=True, verbose_name='Active')

    @property
    def likes(self):
        return self.liked_by.count()

    def is_liked_by(self, user):
        return self.liked_by.filter(id=user).exists()

    def __str__(self):
        return f"{self.author} commented: {self.comment}"