from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView
from rest_framework.documentation import include_docs_urls

from api import urls as api_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(api_urls.urlpatterns)),
    url(r'^docs/', include_docs_urls(title='maze_eval API')),
    url(r'^.*$', RedirectView.as_view(url='/docs/', permanent=False)),
]
