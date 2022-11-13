"""coaph URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include, re_path
from rest_framework import routers
from django.conf.urls.static import static
#from attestation import views as attestation_views
from frontend import views as front_views
#from protheses import views as protheses_views
from django.conf import settings

admin.site.enable_nav_sidebar = False
#router = routers.DefaultRouter()
#router.register(r'attestations', attestation_views.AttestationView, 'attestation')
if not settings.DEBUG :
    handler404 = 'frontend.views.not_found_view'
    handler500 = 'frontend.views.not_found_view'
else:
    pass

urlpatterns = [
    path('', include('frontend.urls')), # frontend URL
    path('grappelli/', include('grappelli.urls')), # grappelli URL
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)