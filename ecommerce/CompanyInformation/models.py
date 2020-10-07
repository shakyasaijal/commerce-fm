from django.db import models


from User import models as user_models


class SocialMedia(user_models.SingletonModel):
    facebook_link = models.URLField(null=True, blank=True)
    twitter_link = models.URLField(null=True, blank=True)
    linkedIn_link = models.URLField(null=True, blank=True)
    instagram_link = models.URLField(null=True, blank=True)
    youtube_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return "Social Media Links"

    class Meta:
        verbose_name = "Social Media"
        verbose_name_plural = "Social Medias"


class ContactNumber(user_models.AbstractTimeStamp):
    number = models.BigIntegerField(null=False, blank=False, unique=True)
    of = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return "{} - {}".format(self.number, self.of)

    class Meta:
        verbose_name = "Contact Number"
        verbose_name_plural = "Contact Numbers"


class CompanyInformation(user_models.SingletonModel):
    email = models.EmailField(null=True, blank=True)
    phone = models.ManyToManyField(
        ContactNumber, blank=True, related_name="company_phone")
    address = models.TextField(null=True, blank=True)
    fax = models.CharField(max_length=255, null=True, blank=True)
    post_box = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return "Company Data"

    class Meta:
        verbose_name = "Company Information"
        verbose_name_plural = "Company Informations"
