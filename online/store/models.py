from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="Category title")
    slug =  models.SlugField(max_length=100, verbose_name="Category slug")
    description = models.TextField(
        blank=True, null=True, verbose_name="Category description"
    )
    game_number = models.IntegerField(default=0 ,blank=True, null=True, verbose_name="Category games number")
    is_active = models.BooleanField(default=True, verbose_name="Is Category active")

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.title
    
def default_category():
    return Category.objects.get(title="default").pk


class Game(models.Model):
    name = models.CharField(max_length=100, verbose_name="Game name")
    pub_date = models.DateField(verbose_name="Game publication date", auto_now_add=True)
    release_date = models.DateField(verbose_name="Release date")
    price = models.DecimalField(
        decimal_places=2, max_digits=6, verbose_name="Game price"
    )
    slug = models.SlugField(max_length=100, verbose_name="Game slug")
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_DEFAULT,
        default=default_category,
    )
    description = models.TextField(default="Game description", verbose_name="Description")
    game_image = models.ImageField(
        upload_to="game", blank=True, null=True, verbose_name="Game image"
    )
    is_active = models.BooleanField(default=True, verbose_name="Is Game active")

    class Meta:
        verbose_name = 'Game'
        verbose_name_plural = 'Games'
        
    def __str__(self):
        return self.name
    
    def img_tag(self):
        from django.utils.html import mark_safe
        return mark_safe(f'<img src = "{self.game_image.url}" width = "300"/>')
    
class Comment(models.Model):
    text = models.CharField(max_length=100, verbose_name="Comment text")
    pub_date = models.DateField(verbose_name="Comment publication date", auto_now_add=True)
    rating = models.IntegerField(verbose_name="Comment rating")
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    
    def get_absolute_url(self):
       return reverse("store:game-detail", kwargs={'game_slug': self.game.slug})
