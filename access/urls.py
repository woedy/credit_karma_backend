from django.urls import path

from access.views import AccessPageView


app_name = 'access'

urlpatterns = [
    path('check-access/', AccessPageView.as_view(), name="access+view"),
]
