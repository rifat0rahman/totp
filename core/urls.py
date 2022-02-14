from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('api/device',views.device,name='device'),
    path("api/authenticate",views.authenticate, name="auth"),

    #templates
    path('',views.auth, name="authen"),
    path("<int:locationID>",views.home, name="home"),
    

]
