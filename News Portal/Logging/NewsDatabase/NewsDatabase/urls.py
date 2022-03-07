from django.contrib import admin
from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('pages/', include('django.contrib.flatpages.urls')),
#     path('news/', include('news.urls')),
# ]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),
    path('sign/', include('sign.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('accounts.urls'))
]
