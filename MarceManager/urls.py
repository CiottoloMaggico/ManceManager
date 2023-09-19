"""
URL configuration for MarceManager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from base.views import ClientListView, ParcelDeleteView, CategoryListView, CategoryDeleteView, ParcelCreateView, ParcelUpdateView, ClientDetailView, ClientDeleteView, ActivityDeleteView, ActivityDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ClientListView.as_view(), name='client_list'),
    path('client/<pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client/<pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
    path('client/<int:id>/activity/<pk>/', ActivityDetailView.as_view(), name='activity_detail'),
    path('client/<int:id>/activity/<pk>/delete/', ActivityDeleteView.as_view(), name='activity_delete'),
    path('client/<int:pk>/parcel/create/', ParcelCreateView.as_view(), name='parcel_create'),
    path('client/<int:id>/parcel/<pk>/update/', ParcelUpdateView.as_view(), name='parcel_update'),
    path('client/<int:id>/parcel/<pk>/delete/', ParcelDeleteView.as_view(), name='parcel_delete'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('category/<pk>/delete/', CategoryDeleteView.as_view(), name='category_delete')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
