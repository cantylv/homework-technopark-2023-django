from main.models import *


def updatePopularTags() -> None:
    object_list = Tag.objects.all()
    for tag in object_list:
        tag.rating = tag.question_set.count()
        tag.save()
