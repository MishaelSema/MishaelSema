from django.urls import path
from . import views

urlpatterns = [
    path('', views.pack_list, name='pack_list'),
    # -------------------------------------------------------------------Normal Sponsors start
    path('subscribe/<int:pack_id>/', views.subscribe, name='subscribe'),
    path('thank_you/', views.thank_you, name='thank_you'),
    # -------------------------------------------------------------------Normal Sponsors end

    # -------------------------------------------------------------------Selection Event plans start
    path('event_items/', views.event_item_selection, name='event_item_selection'),
    path('event_subscribe/', views.event_subscribe, name='event_subscribe'),
    # -------------------------------------------------------------------Selection Event plans end

    # -------------------------------------------------------------------Sponsor Evennt plans start
    path('sponsor_event/', views.event_sponsor, name='event_sponsor'),
    # -------------------------------------------------------------------Sponsor Evennt plans end



]
