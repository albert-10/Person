from datetime import date

from django.db.models.aggregates import Count
from django.db.models.expressions import F
from django.shortcuts import reverse
from django.db.models.functions import Coalesce
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Sum, Count, Prefetch

from .models import Person
from .forms import PersonForm, PersonEditForm

class PersonListView(generic.ListView):    
    template_name = 'personapp/personList.html'    

    # This function return a list of person with their attributes and extra atributes: total_age_children, oldest_child
    # and number of male children and female children

    def get_queryset(self):
        females = Person.objects.filter(gender='female')
        males = Person.objects.filter(gender='male')
        
        # Prefetching children dad, children mom and male and female children related to a person.

        persons = Person.objects.prefetch_related(
            'children_dad',
            'children_mom',
            Prefetch('children_dad', queryset=females, to_attr='children_dad_female'),
            Prefetch('children_dad', queryset=males, to_attr='children_dad_male'),
            Prefetch('children_mom', queryset=females, to_attr='children_mom_female'),
            Prefetch('children_mom', queryset=males, to_attr='children_mom_male')).annotate(
                total_years=Coalesce(Sum('children_dad__date_of_birth__year'), 0) + Coalesce(Sum('children_mom__date_of_birth__year'), 0)).annotate(
                total_children=Coalesce(Count('children_dad__date_of_birth'), 0) + Coalesce(Count('children_mom__date_of_birth'), 0)).annotate(
                years_amount=F('total_children')*date.today().year).annotate(

                # Annotating total age children    
                total_age_children=F('years_amount')-F('total_years'))

         # Annotating oldest_child, children_male_amount and children_male_amount

        for person in persons:                         
            if person.children_mom.all().count() > 0:
                person.oldest_child = person.children_mom.all()[0]
                              
            elif person.children_dad.all().count() > 0:
                person.oldest_child = person.children_dad.all()[0]
            else:
                person.oldest_child = 'No children'
            
            if person.gender == 'male':
                person.children_female_amount = len(person.children_dad_female)
                person.children_male_amount = len(person.children_dad_male)                               
            else:                
                person.children_female_amount = len(person.children_mom_female)
                person.children_male_amount = len(person.children_mom_male)     
       
        return persons

class PersonInsertView(CreateView):
    template_name = 'personapp/personInsert.html'
    form_class = PersonForm
    queryset = Person.objects.all()

    def get_success_url(self):
        return reverse("personapp:personInsert")

class PersonEditView(UpdateView):
    template_name = 'personapp/personEdit.html'
    model = Person
    form_class = PersonEditForm

    # This function return a person as a context with the added atributes: total_age_children, oldest_child
    # and number of male children and female children
    
    def get_context_data(self, **kwargs):             
        context = super().get_context_data(**kwargs)        
        females = Person.objects.filter(gender='female')
        males = Person.objects.filter(gender='male')
        persons = Person.objects.filter(pk=self.kwargs["pk"]).prefetch_related(
            'children_dad',
            'children_mom',
            Prefetch('children_dad', queryset=females, to_attr='children_dad_female'),
            Prefetch('children_dad', queryset=males, to_attr='children_dad_male'),
            Prefetch('children_mom', queryset=females, to_attr='children_mom_female'),
            Prefetch('children_mom', queryset=males, to_attr='children_mom_male')).annotate(
                total_years=Coalesce(Sum('children_dad__date_of_birth__year'), 0) + Coalesce(Sum('children_mom__date_of_birth__year'), 0)).annotate(
                total_children=Coalesce(Count('children_dad__date_of_birth'), 0) + Coalesce(Count('children_mom__date_of_birth'), 0)).annotate(
                years_amount=F('total_children')*date.today().year).annotate(

                # Annotating total age children    
                total_age_children=F('years_amount')-F('total_years'))

        # Annotating oldest_child, children_male_amount and children_male_amount
        person = persons[0]
                                
        if person.children_mom.all().count() > 0:
            person.oldest_child = person.children_mom.all()[0]
                            
        elif person.children_dad.all().count() > 0:
            person.oldest_child = person.children_dad.all()[0]
        else:
            person.oldest_child = 'No children'
        
        if person.gender == 'male':
            person.children_female_amount = len(person.children_dad_female)
            person.children_male_amount = len(person.children_dad_male)                
        else:                
            person.children_female_amount = len(person.children_mom_female)
            person.children_male_amount = len(person.children_mom_male)        

        context['person'] = person
        return context

class PersonDeleteView(DeleteView):    
    model = Person
    success_url = reverse_lazy('personapp:personList')
    
    