from django.urls import path,include
from . import views
from .views import *
urlpatterns = [
    path('', Home, name='home'),
    #path('login', views.logIn, name='login'),
    path('login2', login_page, name='login2'),
    path('logout', dcx, name='logout'),
    #path('register', register.as_view(), name='register'),
    path('register2', register, name='register2'),
    #path('PDF', some_view, name='PDF'),
    path('detailVoy/res/<int:num>', res.as_view(), name='res'),
    path('pdff',GeneratePdf.as_view(),name='pdff'),
    path('apropos', apropos, name='apropos'),
    #path('test', test, name='test'),
    #path('bonjour', bonjour, name='bonjour'),
    path('contact', contact.as_view(), name='contact'),
    path('listeVoyage', views.ListeVoyage.as_view(), name='listeVoyage'),
    path('listeMessages', views.ListeMessages.as_view(), name='listeMessages'),
    path('detailVoy/<int:num>', detailVoy.as_view(), name='detailVoy'),
    #path('nvUtil', views.NewUtil.as_view(), name='nvUtil'),
    
]
