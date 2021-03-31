"""Eshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls.static import static
from store import views
from . import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.index, name='home'),
                  path('signup/', views.signup,name='signup'),
                  path('login/', views.login, name='login'),
                  path('activation/<int:user_id>/', views.activation, name='activation'),
                  path('logout/', views.logout),
                  path('cart/', views.cart, name='cart'),
                  path('check-out/', views.check_out),
                  path('clear/', views.clear),
                  path('order/', views.order, name='orders'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
