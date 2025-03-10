"""
URL configuration for cluckbox project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from cluckbox import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",views.signup,name='signup'),
    path("login/",views.login,name='login'),
    path("home/",views.home,name='home'),
    path("order/",views.order,name='order'),
    path("dashboard/",views.dashboard,name='dashboard'),
    #path("akdashboard/",views.akdashboard,name='akdashboard'),
    path("about/",views.about,name='about'),
    path("contact/",views.contact,name='contact'),
    path("delete/",views.delete,name='delete'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
   # path('clear_cart/', views.clear_cart, name='clear_cart'),
]
