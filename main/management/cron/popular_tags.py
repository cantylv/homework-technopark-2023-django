from main.models import *
from django.core.cache import cache


def updatePopularTags() -> None:
    object_list = Tag.objects.all()
    for tag in object_list:
        tag.rating = tag.question_set.count()
        tag.save()

    cache.set('popular_tags', Tag.objects.order_by('-rating')[:20], 3600 * 24 * 31 * 3.1)  # кешируем на 3 месяца
