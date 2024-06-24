from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


#------------------------------------------------------------------------NORMAL SPONSORS
class Item(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Pack(models.Model):
    name = models.CharField(max_length=100)
    amount_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.ManyToManyField(Item)

    def __str__(self):
        return self.name



class Subscription(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    COMPANY_TYPE_CHOICES = [
        ('TPE', 'Très Petite Entreprise'),
        ('PMI', 'Petite et Moyenne Industrie'),
        ('PME', 'Petite et Moyenne Entreprise'),
        ('StartUp', 'StartUp'),
        ('Autres', 'Autres'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    pack = models.ForeignKey(Pack, on_delete=models.CASCADE, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    company_name = models.CharField(max_length=255)
    company_type = models.CharField(max_length=10, choices=COMPANY_TYPE_CHOICES)
    creation_date = models.DateField()
    items = models.ManyToManyField(Item, blank=True)
    amount_per_month = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Check if the instance is new

        if is_new:
            super().save(*args, **kwargs)  # Save the instance to generate a primary key

            if self.pack:
                self.items.set(self.pack.description.all())
                self.amount_per_month = self.pack.amount_per_month
                super().save(update_fields=['amount_per_month'])  # Save the updated amount_per_month

            self.send_subscription_email()  # Send the email after saving the amount_per_month
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        if self.pack:
            return f"{self.first_name} - {self.pack.name}"
        else:
            return f"{self.first_name} - No Pack Assigned"

    def send_subscription_email(self):
        subject_user = 'Your Subscription Details'
        subject_admin = 'New Subscription Notification'

        pack_name = self.pack.name
        items_list = ', '.join([item.name for item in self.items.all()])

        context = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'address': self.address,
            'pack_name': pack_name,
            'amount_per_month': self.amount_per_month,
            'items_list': items_list,
            'company_name': self.company_name,
            'company_type': self.company_type,
        }

        message_for_user = render_to_string('emails/subscription_user.html', context)
        message_for_admin = render_to_string('emails/subscription_admin.html', context)

        send_mail(subject_user, '', settings.EMAIL_HOST_USER, [self.email], html_message=message_for_user)
        send_mail(subject_admin, '', settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], html_message=message_for_admin)

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'

#------------------------------------------------------------------------EVENT OFFER SPONSORS
class EventItem(models.Model):
    CATEGORY_CHOICES = [
        ('Event Brochure', 'Event Brochure'),
        ('Event Catalog', 'Event Catalog'),
        ('Event Promotion Campaign', 'Event Promotion Campaign'),
        ('Branding Rights', 'Branding Rights'),
        ('Logo Visibility', 'Logo Visibility'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.category}"
    def get_category_display(self):
        return dict(self.CATEGORY_CHOICES).get(self.category, 'Unknown Category')

class EventSubscription(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    COMPANY_TYPE_CHOICES = [
        ('TPE', 'Très Petite Entreprise'),
        ('PMI', 'Petite et Moyenne Industrie'),
        ('PME', 'Petite et Moyenne Entreprise'),
        ('StartUp', 'StartUp'),
        ('Autres', 'Autres'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    company_name = models.CharField(max_length=255)
    company_type = models.CharField(max_length=10, choices=COMPANY_TYPE_CHOICES)
    creation_date = models.DateField()
    event_items = models.ManyToManyField(EventItem)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk is None:  # New instance
            super().save(*args, **kwargs)  # Save the instance to generate a primary key
            self.total_price = sum(item.price for item in self.event_items.all())
            super().save(update_fields=['total_price'])  # Save the updated total_price
            self.send_subscription_email()  # Send the email after saving
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Event Subscription"

    def send_subscription_email(self):
        subject_user = 'Your Event Subscription Details'
        subject_admin = 'New Event Subscription Notification'

        event_items_list = [
            {'name': item.name, 'category': item.get_category_display()} for item in self.event_items.all()
        ]

        context = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'address': self.address,
            'company_name': self.company_name,
            'company_type': self.company_type,
            'event_items_list': event_items_list,
            'total_price': self.total_price,
        }

        message_for_user = render_to_string('emails/event_subscription_user.html', context)
        message_for_admin = render_to_string('emails/event_subscription_admin.html', context)

        if self.total_price > 0:
            send_mail(subject_user, '', settings.EMAIL_HOST_USER, [self.email], html_message=message_for_user)
            send_mail(subject_admin, '', settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], html_message=message_for_admin)

    class Meta:
        verbose_name = 'Event Subscription'
        verbose_name_plural = 'Event Subscriptions'

#------------------------------------------------------------------------SUPPORT SPONSORS
class SponsorEvent(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    SPONSOR_EVENTS = [
        ('Registration Desk', 'Registration Desk'),
        ('Delegate Lunches', 'Delegate Lunches'),
        ('Delegate Coffee Breaks', 'Delegate Coffee Breaks'),
        ('Networking Dinner', 'Networking Dinner'),
        ('Closing Reception', 'Closing Reception'),
        ('Lanyards & Badges', 'Lanyards & Badges'),
    ]

    sponsor_first_name = models.CharField(max_length=200)
    sponsor_last_name = models.CharField(max_length=200)
    event_name = models.CharField(max_length=200, choices=SPONSOR_EVENTS)
    support_amount = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return f"{self.sponsor_first_name} {self.sponsor_last_name} - {self.event_name}"

    def send_sponsor_email(self):
        subject_user = 'Thank You for Your Support'
        subject_admin = 'New Event Support Notification'

        context = {
            'sponsor_first_name': self.sponsor_first_name,
            'sponsor_last_name': self.sponsor_last_name,
            'event_name': self.event_name,
            'support_amount': self.support_amount,
            'email': self.email,
            'phone_number': self.phone_number,
            'address': self.address,
            'gender': self.gender,
        }

        message_for_user = render_to_string('emails/sponsor_event_user.html', context)
        message_for_admin = render_to_string('emails/sponsor_event_admin.html', context)

        send_mail(subject_user, '', settings.EMAIL_HOST_USER, [self.email], html_message=message_for_user)
        send_mail(subject_admin, '', settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], html_message=message_for_admin)

    class Meta:
        verbose_name = 'Sponsor Event'
        verbose_name_plural = 'Sponsor Events'