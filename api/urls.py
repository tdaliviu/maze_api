from django.conf.urls import url
from rest_framework_expiring_authtoken import views as rest_framework_views

from api import views

urlpatterns = [
    url(r'^token/', rest_framework_views.obtain_expiring_auth_token),
    url(r'^user/', views.UserList.as_view()),
    url(r'^snippet/', views.SnippetList.as_view()),
]
