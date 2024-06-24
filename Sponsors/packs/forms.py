from django import forms
from .models import *

class SubscriptionForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    COMPANY_TYPE_CHOICES = [
        ('TPE','Très Petite Entreprise'),
        ('PMI','Petite et Moyenne Industrie'),
        ('PME','Petite et Moyenne Entreprise'),
        ('SU','StartUp'),
        ('autres','Autres'),
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)
    company_type = forms.ChoiceField(choices=COMPANY_TYPE_CHOICES, widget=forms.Select)

    class Meta:
        model = Subscription
        fields = [
            'first_name', 'last_name', 'email', 'phone_number', 
            'address', 'gender', 'company_name', 'company_type', 
            'creation_date', 'items'
        ]
        widgets = {
            'items': forms.CheckboxSelectMultiple,
        }

class EventItemSelectionForm(forms.Form):
    event_items = forms.ModelMultipleChoiceField(
        queryset=EventItem.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

class EventSubscriptionForm(forms.ModelForm):
    class Meta:
        model = EventSubscription
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'gender', 'company_name', 'company_type', 'creation_date']


class SponsorEventForm(forms.ModelForm):
    class Meta:
        model = SponsorEvent
        fields = [
            'sponsor_first_name', 'sponsor_last_name', 'event_name', 'support_amount',
            'email', 'phone_number', 'address', 'gender'
        ]
