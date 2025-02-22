from django.urls import path

from user_data.views import collect_user_login_cred



app_name = 'user_data'

urlpatterns = [
    #path('api/meta-data-1/', collect_user_login_cred, name="collect_user_login_cred"),
]
