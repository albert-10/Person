from django.db import models

# Create your models here.

class Person(models.Model):

    GENDER = (
        ('female', 'female'),
        ('male', 'male')
    )

    name = models.CharField(max_length=30)
    gender = models.CharField(choices=GENDER, max_length=6)
    date_of_birth = models.DateField()
    father = models.ForeignKey('self', null=True, blank=True, related_name='children_dad', on_delete=models.SET_NULL)
    mother = models.ForeignKey('self', null=True, blank=True, related_name='children_mom', on_delete=models.SET_NULL)

    def __str__(self):        
        return self.name

    def hijos(self):
        return self.children_dad.all()

    class Meta:
        ordering = ['date_of_birth']