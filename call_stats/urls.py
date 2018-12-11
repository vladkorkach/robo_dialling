from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name="index"),
    # path("call/", views.debug_call_route, name="debug"),
    path('callback/', views.twilio_callback, name="callback"),
    # path("xml-voice.xml", views.xml_voice, name="xml")
]
