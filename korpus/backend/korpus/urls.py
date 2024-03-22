from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic.base import RedirectView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .jwt import RichTokenObtainPairView
from .views import serve_media_file, get_config

api_info = openapi.Info(
    title="Korpus API",
    default_version='v1',
    description="Korpus API Description",
    terms_of_service="https://rsj.rs/",
    contact=openapi.Contact(email="mbranko@uns.ac.rs"),
    license=openapi.License(name="GPL v3 License"),
)

schema_view = get_schema_view(
   openapi.Info(
      title="Korpus API",
      default_version='v1',
      description="Korpus API Description",
      terms_of_service="https://rsj.rs/",
      contact=openapi.Contact(email="mbranko@uns.ac.rs"),
      license=openapi.License(name="GPL v3 License"),
   ),
   public=False,
   permission_classes=(IsAuthenticated,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', RichTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/config/', get_config),
    path('api/reci/', include('reci.urls', namespace='reci')),
    path('api/publikacije/', include('publikacije.urls', namespace='publikacije')),
    path('api/pretraga/', include('indexer.urls', namespace='pretraga')),
    path('api/decider/', include('decider.urls', namespace='decider')),
    path('api/recnikproxy/', include('recnikproxy.urls', namespace='recnikproxy')),
    path(r'swagger<str:format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('media/<path:file_path>/', serve_media_file),
    path('', RedirectView.as_view(url=reverse_lazy('admin:index')))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
