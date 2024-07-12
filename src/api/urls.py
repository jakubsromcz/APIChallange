from django.urls import path
from .views import CountryListCreateAPIView, CountryRetrieveUpdateAPIView

urlpatterns = [
    path('countries/', CountryListCreateAPIView.as_view(), name='country-list-create'),
    path('countries/<int:pk>/', CountryRetrieveUpdateAPIView.as_view(), name='country-retrieve-update'),
]
