from django.conf.urls import url
from django.contrib import admin
from rest_framework_expiring_authtoken import views as rest_framework_views

from maze_eval import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^token/', rest_framework_views.obtain_expiring_auth_token),
    url(r'^user/', views.UserList.as_view()),
    url(r'^snippet/', views.SnippetList.as_view()),
]
