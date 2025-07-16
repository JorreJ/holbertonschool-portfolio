from django.urls import path, include

urlpatterns = [
    path('', include('lighthouse.urls')),
]