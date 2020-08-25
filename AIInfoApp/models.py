from django.db import models

# Create your models here.


class AiClass(models.Model):
    class_num = models.IntegerField()
    lecturer = models.CharField(max_length=30)


class AiStudents(models.Model):
    class_num = models.IntegerField()
    name = models.CharField(max_length=30)
    phone_num = models.CharField(max_length=15,  blank=True)
    intro_text = models.TextField(null=True, default=' ')
