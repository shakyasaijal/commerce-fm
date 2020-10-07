from django.db import models

from User import models as user_models


class SearchedKeyWord(user_models.AbstractTimeStamp):
    # If user, authenticated
    user = models.ForeignKey("User.User", on_delete=models.CASCADE, null=True, blank=True)

    # If not authenticated
    ip = models.ForeignKey("User.IpAddress", on_delete=models.SET_NULL, null=True, blank=True)
    keyword = models.CharField(max_length=255, null=False, blank=False, unique=True)
    count = models.BigIntegerField(null=False, blank=False, default=0)

    def __str__(self):
        return "Keyword: {}, Count: {}".format(self.keyword, self.count)

    class Meta:
        verbose_name = "Searched Keyword"
        verbose_name_plural = "Searched Keywords"
    
