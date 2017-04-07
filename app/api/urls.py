from django.conf.urls import url
from rest_framework.documentation import include_docs_urls
from rest_framework_expiring_authtoken import views as rest_framework_views

from api import views

urlpatterns = [
    url(r'^docs/', include_docs_urls(title='maze_eval API')),
    url(r'^tokens/$', rest_framework_views.obtain_expiring_auth_token),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^snippets/$', views.SnippetList.as_view()),
    url(r'^overall_scoreboard/$', views.ScoreList.as_view()),
]
