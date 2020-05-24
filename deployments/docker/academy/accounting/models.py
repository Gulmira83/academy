from django.db import models

class Plans(models.Model):
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=20)
    description = models.CharField(max_length=250)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "plans"





    