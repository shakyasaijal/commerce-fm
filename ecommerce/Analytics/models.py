from django.db import models

from User import models as user_models


class SearchedKeyWord(user_models.AbstractTimeStamp):
    keyword = models.CharField(max_length=255, null=False, blank=False, unique=True)
    count = models.BigIntegerField(null=False, blank=False, default=0)

    def __str__(self):
        return self.keyword

    class Meta:
        verbose_name = "Searched Keyword"
        verbose_name_plural = "Searched Keywords"
        