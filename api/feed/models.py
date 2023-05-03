from django.db import models

"""BaseModel"""


class BaseModel(models.Model):
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)


"""Other Models"""


class Genre(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=80)

    @property
    def manga_count(self):
        return self.manga_set.count()

    def manga_list(self):
        return [manga.title for manga in self.manga_set.all()]

    def __str__(self):
        return self.name


class Manga(BaseModel):
    title = models.CharField(max_length=80)
    description = models.TextField()
    published = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title

    # properties
    @property
    def reviews_list(self):
        return [review.text for review in self.reviews.all()]

    @property
    def genres_list(self):
        return [genre.name for genre in self.genres.all()]

    @property
    def category_name(self):
        try:
            return self.category.name
        except Category.DoesNotExist:
            return ""

    @property
    def rating(self):
        try:
            stars_list = [review.stars for review in self.reviews.all()]
            return round(sum(stars_list) / len(stars_list), 2)
        except ZeroDivisionError:
            return 0


class Review(models.Model):
    CHOICES = ((i, "*" * i) for i in range(1, 6))
    text = models.TextField()
    stars = models.IntegerField(choices=CHOICES, default=1)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, related_name="reviews")
