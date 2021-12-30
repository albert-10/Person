from django import forms
from .models import Person

class PersonForm(forms.ModelForm):
    
    class Meta:
        model = Person
        fields = '__all__'

    # Put just female in the field mother and male in the field father

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mother'].queryset = Person.objects.filter(gender='female')
        self.fields['father'].queryset = Person.objects.filter(gender='male')

class PersonEditForm(forms.ModelForm):
    
    class Meta:
        model = Person
        fields = '__all__'

    # Put just female in the field mother and male in the field father. Avoid a person himself be its father or mother, as well as its children can not be
    # its parents

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        self.fields['mother'].queryset = Person.objects.filter(gender='female').exclude(id=self.instance.id).exclude(mother__id=self.instance.id)
        self.fields['father'].queryset = Person.objects.filter(gender='male').exclude(id=self.instance.id).exclude(father__id=self.instance.id)
