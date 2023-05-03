from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError

"""Model Serializers"""


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "id name manga_count manga_list".split()


class MangaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manga
        fields = (
            "id title description rating category_name genres_list published".split()
        )


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "id stars text product_title".split()


"Validate Serializer"


class ValidateMangaSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=80)
    description = serializers.CharField(required=False)
    published = serializers.DateField()
    category_id = serializers.IntegerField()
    genres = serializers.ListField(child=serializers.IntegerField())

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError("Category not found!")
        return category_id

    def validate_genres(self, genres):
        filtered_tags = Genre.objects.filter(id__in=genres)  # QuerySet of existed tags
        if len(genres) == filtered_tags.count():  # validating
            return genres

        lst_ = {
            i["id"] for i in filtered_tags.values_list().values()
        }  # creating set of existed tags

        raise ValidationError(
            f"This ids doesnt exist {set(genres).difference(lst_)}"
        )  # collecting errors


class ValidateReviewSerializer(serializers.Serializer):
    text = serializers.Serializer(required=False)
    stars = serializers.IntegerField(min_value=1, max_value=5)
    product_id = serializers.IntegerField()

    def validate_product_id(self, product_id):
        try:
            Review.objects.get(product_id=product_id)
        except Review.DoesNotExist:
            raise ValidationError("Review doesnt exist")


class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField()
