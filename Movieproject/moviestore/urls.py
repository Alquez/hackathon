"""moviestore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from movie_api.views import MovieViewSet, ReviewViewSet

schema_view = get_schema_view(
    info=openapi.Info(
        title='Blog Project',
        default_version='v1',
        description='this is test blog project',
        terms_of_service='http://www.google.com/policies/terms/',
        contact=openapi.Contact(email='test@gmail.com'),
        license=openapi.License(name='BSD License')
    ),
    public=True,
    permission_classes=(permissions.AllowAny, ),
)

router = DefaultRouter()
router.register('movie', MovieViewSet)
router.register('review', ReviewViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/docs/', schema_view.with_ui()),
    # path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/v1/accounts/', include('user.urls'),),
    path('api/v1/profile/', include('movieprofile.urls')),
    path('api/v1/', include('movie_api.urls')),
    path('api/v1/', include(router.urls)),
]

urlpatterns += static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)
urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)