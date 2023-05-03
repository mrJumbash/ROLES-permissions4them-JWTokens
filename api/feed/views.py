from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from .serializers import *
from .models import *
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .service import MovieFilter


"""Manga"""


class MangaListCreateAPI(generics.ListCreateAPIView):
    serializer_class = MangaSerializer
    queryset = Manga.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ("title",)
    filterset_class = MovieFilter

    def post(self, request, *args, **kwargs):
        serializer = ValidateMangaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        title = serializer.validated_data.get("title")
        description = serializer.validated_data.get("description")
        published = serializer.validated_data.get("published")
        category_id = serializer.validated_data.get("category_id")
        genres = serializer.validated_data.get("genres")
        manga = Manga.objects.create(
            title=title,
            description=description,
            published=published,
            category_id=category_id,
        )
        manga.genres.set(genres)
        manga.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MangaDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MangaSerializer
    queryset = Manga.objects.all()
    pagination_class = PageNumberPagination
    lookup_field = "id"

    def put(self, request, *args, **kwargs):
        serializer = ValidateMangaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        manga = Manga.objects.all()
        manga.title = serializer.validated_data.get("title")
        manga.description = serializer.validated_data.get("description")
        manga.published = serializer.validated_data.get("published")
        manga.category_id = serializer.validated_data.get("category_id")
        manga.genres = serializer.validated_data.get("genres")
        manga.save()
        return Response(data=MangaSerializer(manga).data)


"""Review"""


class ReviewListCreateAPI(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    pagination_class = PageNumberPagination

    def post(self, request, *args, **kwargs):
        serializer = ValidateReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        text = serializer.validated_data.get("text")
        manga_id = serializer.validated_data.get("product_id")
        stars = serializer.validated_data.get("stars")
        reviews = Review.objects.create(text=text, stars=stars, manga_id=manga_id)
        reviews.save()
        return Response(data=ReviewSerializer(reviews).data)


class ReviewDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    lookup_field = "id"

    def put(self, request, *args, **kwargs):
        serializer = ValidateReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = Review.objects.all()

        review.text = serializer.validated_data.get("text")
        review.product_id = serializer.validated_data.get("product_id")
        review.stars = serializer.validated_data.get("stars")
        review.save()
        return Response(data=ReviewSerializer(review).data)


"""Category"""


class CategoryAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination

    def post(self, request, *args, **kwargs):
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data.get("name")
        category = Category.objects.create(name=name)
        return Response(data=CategorySerializer(category).data)
