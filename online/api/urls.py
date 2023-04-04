from django.urls import path, re_path, include
from rest_framework_simplejwt.views import (
TokenObtainPairView,
TokenRefreshView,
)
from . import views

from drf_yasg.views import get_schema_view  # new
from drf_yasg import openapi  # new
from rest_framework import permissions


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('games/', views.GetGameInfoView.as_view()),
    re_path('^games/(?P<category>.+)/$', views.GetCategoryGameInfoView.as_view()),
    path('filter-games/', views.GetGameInfoFilterView.as_view()),
    path('search-games/', views.GetGameInfoSearchView.as_view()),
    path('order-games/', views.GetGameInfoOrderView.as_view()),
    path('custom-filter-games/', views.GetGameInfoFilterSetView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]