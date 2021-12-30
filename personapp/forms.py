from django import forms
from .models import Person

class PersonForm(forms.ModelForm):
    
    class Meta:
        model = Person
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mother'].queryset = Person.objects.filter(gender='female')
        self.fields['father'].queryset = Person.objects.filter(gender='male')