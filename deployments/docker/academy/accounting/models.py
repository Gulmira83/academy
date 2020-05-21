from django.db import models


# Create your models here.

# class Account(models.Model):
#     name        = models.CharField(max_length=200)
#     servces     = models.Arr

#     class Meta:
#         managed     = True
#         ordering    = ['name']


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


# class Features(models.Model):
#     option1 = models.CharField(max_length=200)
#     option2 = models.CharField(max_length=200)
#     option3 = models.CharField(max_length=200)

#     plan = models.ForeignKey(Plans, on_delete=models.CASCADE) 

#     def __str__(self):
#         return self.option1
       

#     class Meta:
#         verbose_name_plural = "features"


    