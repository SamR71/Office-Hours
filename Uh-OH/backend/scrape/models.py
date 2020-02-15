from django.db import models

# Create your models here.
class Search(models.Model):
    searchValue = models.CharField(max_length=500)
    createTime = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Searches'

    def __str__(self):
        return self.searchValue


