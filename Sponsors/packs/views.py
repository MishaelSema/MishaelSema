from django.shortcuts import render, redirect
from collections import defaultdict
from .models import *
from .forms import *

def pack_list(request):
    packs = Pack.objects.all()
    items = Item.objects.all()
    return render(request, 'packs/pack_list.html', {'packs': packs, 'items': items})

def subscribe(request, pack_id=None):
    selected_event_items = request.session.get('selected_event_items', [])

    if pack_id:
        pack = Pack.objects.get(id=pack_id)
    else:
        pack = None

    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            if pack:
                subscription.pack = pack
                subscription.save()
                subscription.items.set(pack.description.all())
            else:
                subscription.save()
                selected_items = EventItem.objects.filter(id__in=selected_event_items)
                subscription.items.set(selected_items)
                subscription.amount_per_month = subscription.calculate_price()
            form.save_m2m()
            return redirect('thank_you')
    else:
        form = SubscriptionForm()

    return render(request, 'packs/subscribe.html', {'form': form, 'pack': pack})

def thank_you(request):
    return render(request, 'packs/thank_you.html')

def event_item_selection(request):
    event_items = EventItem.objects.all()
    categorized_items = defaultdict(list)
    for item in event_items:
        categorized_items[item.category].append(item)
    
    if request.method == 'POST':
        form = EventItemSelectionForm(request.POST)
        if form.is_valid():
            selected_items = form.cleaned_data['event_items']
            request.session['selected_event_items'] = [item.id for item in selected_items]
            pack_id = request.session.get('pack_id')
            if pack_id:
                return redirect('subscribe', pack_id=pack_id)
            else:
                return redirect('event_subscribe')
    else:
        form = EventItemSelectionForm()

    return render(request, 'packs/event_item_selection.html', {'form': form, 'event_items': dict(categorized_items)})


def event_subscribe(request):
    if request.method == 'POST':
        form = EventSubscriptionForm(request.POST)
        if form.is_valid():
            event_subscription = form.save(commit=False)
            selected_event_items_ids = request.session.get('selected_event_items', [])
            selected_event_items = EventItem.objects.filter(id__in=selected_event_items_ids)
            event_subscription.save()
            event_subscription.event_items.set(selected_event_items)
            event_subscription.total_price = sum(item.price for item in selected_event_items)
            event_subscription.save(update_fields=['total_price'])
            event_subscription.send_subscription_email()
            return redirect('thank_you')
    else:
        form = EventSubscriptionForm()

    return render(request, 'packs/event_subscribe.html', {'form': form})

def event_sponsor(request):
    if request.method == 'POST':
        form = SponsorEventForm(request.POST)
        if form.is_valid():
            sponsor_event = form.save()
            sponsor_event.send_sponsor_email()
            return redirect('thank_you')
    else:
        form = SponsorEventForm()
    
    return render(request, 'packs/sponsor_event.html', {'form': form})


