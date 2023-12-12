from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('Log_in/', Log_in, name='Log_in'),
    path('log_out/', log_out, name='log_out'),
    path('Registration/', Registration, name='Registration'),
    path('verify/<auth_token>/', verify, name='verify'),
    path('about/',aboutus,name='about'),
    path('contact/', contact, name='contact'),
]
