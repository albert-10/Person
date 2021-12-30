from django.db import models
from django.shortcuts import reverse
from django.core.exceptions import ValidationError

# Validate a father be a male

def validate_father_gender(value):
    if Person.objects.get(pk=value).gender=='male':        
        return value
    else:
        raise ValidationError("Fathers are male")

# Validate a mother be a female

def validate_mother_gender(value):
    if Person.objects.get(pk=value).gender=='female':        
        return value
    else:
        raise ValidationError("Mothers are female")

class Person(models.Model):

    GENDER = (
        ('female', 'female'),
        ('male', 'male')
    )

    name = models.CharField(max_length=30)
    gender = models.CharField(choices=GENDER, max_length=6)
    date_of_birth = models.DateField()
    father = models.ForeignKey('self', null=True, blank=True, related_name='children_dad', on_delete=models.SET_NULL, validators=[validate_father_gender])
    mother = models.ForeignKey('self', null=True, blank=True, related_name='children_mom', on_delete=models.SET_NULL,  validators=[validate_mother_gender])

    def __str__(self):        
        return self.name    

    def get_absolute_url(self):
        return reverse("personapp:personEdit", kwargs={'pk': self.id})

    class Meta:
        ordering = ['date_of_birth']