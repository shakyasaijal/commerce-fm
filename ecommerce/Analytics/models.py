from django.db import models

from User import models as user_models


class SearchedKeyWord(user_models.AbstractTimeStamp):
    # If user, authenticated
    user = models.ForeignKey("User.User", on_delete=models.CASCADE, null=True, blank=True)

    # If not authenticated
    ip = models.GenericIPAddressField(protocol="both", unpack_ipv4=False, null=True, blank=True, unique=True)
    keyword = models.CharField(max_length=255, null=False, blank=False, unique=True)
    count = models.BigIntegerField(null=False, blank=False, default=0)

    def __str__(self):
        return "Keyword: {}, Count: {}".format(self.keyword, self.count)

    class Meta:
        verbose_name = "Searched Keyword"
        verbose_name_plural = "Searched Keywords"
    

class SearchedAnalytics(user_models.AbstractTimeStamp):
    # If user, authenticated
    user = models.OneToOneField("User.User", on_delete=models.CASCADE, null=False, blank=False)

    # If not authenticated
    ip = models.GenericIPAddressField(protocol="both", unpack_ipv4=False, null=True, blank=True, unique=True)
    keyword = models.ManyToManyField(SearchedKeyWord, related_name="keyword_analytics")

    def __str__(self):
        if self.user:
            return self.user.get_full_name()
        else:
            return self.ip

    class Meta:
        verbose_name = "Search Analytic"
        verbose_name_plural = "Search Analytics"
        